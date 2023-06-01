
import src.database.db as database
from src.api.message import Message
import logging
import src.connectors.openstack_conector as openstack

CLOUD_SUP_TYPES={"openstack","aws"}
ClOUD_OBG_PARAMETERS={"name", "type", "payload"}
OS_PAYLOAD_PARAMETERS={"region_name","auth"}
OS_ACC_AUTH_PARAMETERS={"username", "password", "auth_url", "project_name", "user_domain_name", "project_domain_name"}
OS_OBG_AUTH_PARAMETERS={"username", "password", "auth_url", "project_name"}



def add_cloud(req):
	m = Message()
	flag, m = verify_req(req,m)
	if flag: 
		match req["type"]:
			case "openstack":
				try: 
					openstack.create_openstack_yaml(req["name"],req["payload"])
				except Exception as err: 
					m.reply= "Creating the openstack yaml file failed for the following reason: %s" % err
			case "aws": 
				pass
				# funtion to be implemented
		database.add_cloud_item(req)
	if m.reply == "":
		# TODO: improve this and check for failures on get servers and get securuity groups
		newreq={"name":req["name"],"type":req["type"]}
		get_servers(newreq)
		get_security_groups(newreq)
		m.status = "SUCCESS!"		
	return m.cast_dict()

def get_servers(req):
	m = Message()
	match req["type"]:
		case "openstack":
			try:
				servers=openstack.get_servers(req["name"])
			except Exception as err:
				m.reply= "Collecting the servers from %s cloud resulted in the following exception: %s" % (req["name"],err)
				logging.exception(err)
		case "aws": 
				pass
				# funtion to be implemented
	for server in servers:
		database.add_server_item(server.__dict__)
	if m.reply == "": 
		m.status = "SUCCESS!"
		servers_names=", ".join([server.name for server in servers])
		m.reply = "Collected the following serveres:\n %s" % servers_names	
	return m.cast_dict()

def get_security_groups(req):
	m = Message()
	match req["type"]:
		case "openstack":
			try:
				security_groups = openstack.get_security_groups(req["name"])
			except Exception as err:
				m.reply= "Collecting the security groups from %s cloud resulted in the following exception: %s" % (req["name"],err)
				logging.exception(err)
		case "aws": 
				pass
				# funtion to be implemented
	for sg in security_groups: 
		database.add_sg_item(sg.to_dict())
	if m.reply == "": 
		m.status = "SUCCESS!"
		sg_names=", ".join([sg.name for sg in security_groups])
		m.reply = "Collected the following security groups:\n %s" % sg_names	
	return m.cast_dict()

def create_security_group(req):
	m = Message()
	match req["type"]:
		case "openstack":
			try:
				security_group = openstack.create_security_group(req["provider"],req["name"])
				update_m = update_security_groups({"name": req["provider"], "type" : req["type"]})
				logging.info("Updating the security groups after adding a new group. The returned messages %s" % update_m)
			except Exception as err:
				m.reply= "Creating the security group %s resulted in the following exception: %s" % (req["name"],err)
				logging.exception(err)
		case "aws": 
			pass
			# funtion to be implemented
	if m.reply == "": 
		m.status = "SUCCESS!"
		m.data = security_group
	return m.cast_dict()

def update_security_groups(req):
	m = Message()
	match req["type"]:
		case "openstack":
			try:
				security_groups = openstack.get_security_groups(req["name"])
			except Exception as err:
				m.reply= "Collecting the security groups from %s cloud resulted in the following exception: %s" % (req["name"],err)
				logging.exception(err)
		case "aws": 
				pass
				# funtion to be implemented
	db_sg_ids = database.get_sg_ids()
	added_sg_names = []
	for sg in security_groups:
		if sg.id not in db_sg_ids:
			added_sg_names.append(sg.name) 
			database.add_sg_item(sg.to_dict())
	if m.reply == "": 
		m.status = "SUCCESS!"
		if added_sg_names:
			sg_names=", ".join(added_sg_names)
			m.reply = "added the following security groups to the database:\n %s" % sg_names	
		else: 
			m.reply = "No new security groups were found, nothing added to the database"
	return m.cast_dict()

def add_security_group_rule(req):
	m = Message()
	match req["type"]:
		case "openstack":
			try:
				added_rule = openstack.open_port(req["provider"],req["sg_id"],req["port"])
			except Exception as err:
				m.reply= "adding the security group rule to group %s resulted in the following exception: %s" % (req["sg_id"],err)
				logging.exception(err)
		case "aws": 
				pass
	if m.reply == "": 
		m.status = "SUCCESS!"
		m.data = added_rule
	return m.cast_dict()

def open_ip(req):
	m = Message()
	match req["type"]:
		case "openstack":
			try:
				added_rules = openstack.open_ip(req["provider"], req["sg_id"], req["ip"])
			except Exception as err:
				m.reply= "adding the security group rule to group %s resulted in the following exception: %s" % (req["sg_id"],err)
				logging.exception(err)
		case "aws": 
				pass
	if m.reply == "": 
		m.status = "SUCCESS!"
		m.data = added_rules
	return m.cast_dict()

def add_to_cluster(req): 
	m = Message()
	if "ip" not in req.keys(): 
		m.reply= "the request does not have the ip!"
	else: 
		server_query=database.get_server_by_ip(req["ip"])
		if not len(server_query): 
			m.reply= "the ip address does not exist"
		else:
			server          = server_query[0]
			server_ip       = server["address"]			
			server_sg       = database.get_server_sg(server)
			server_provider_name = server["provider_name"]
			server_provider_type = server["provider_type"]
			registered_ip_set  = database.get_cluster_ips()
			registered_sg_set  = database.get_cluster_sgs()
			
			# open all the registered ips of the cluster to the newly added server
			for ip in registered_ip_set: 
				open_ip_req={}
				open_ip_req["type"]=server_provider_type
				open_ip_req["provider"]=server_provider_name
				open_ip_req["sg_id"]=server_sg["id"]
				open_ip_req["ip"]=ip
				open_ip(open_ip_req)

			# open the newly added server ip in all the registered servers
			for sg in registered_sg_set: 
				open_ip_req={}
				open_ip_req["type"]=sg["provider_type"]
				open_ip_req["provider"]=sg["provider_name"]
				open_ip_req["sg_id"]=sg["id"]
				open_ip_req["ip"]=server_ip
				open_ip(open_ip_req)

			database.add_ip_to_cluster(server)
			database.add_sg_to_cluster(server,server_sg)
	return m

def verify_req(req,m): 
	if not ClOUD_OBG_PARAMETERS == set(req.keys()): 
		m.reply = "The request keys \'%s\' don't match the accepted keys \'%s\'" % (str(set(req.keys())),str(ClOUD_OBG_PARAMETERS))

	elif req["type"] not in CLOUD_SUP_TYPES: 
		m.reply = "The cloud type \'%s\' is not supported." % req["type"]

	elif req["name"] == "" : 
		m.reply = "The cloud name should not be empty"

	else: 
		match req["type"]:
			case "openstack": 
				return verify_req_os(req["payload"],m)
			case "aws": 
				return verify_req_aws(req["payload"],m)
	
	return False,m

def verify_req_os(payload,m):
	flag= True
	if not OS_PAYLOAD_PARAMETERS == set(payload.keys()):
		m.reply = "The request payload keys \'%s\' don't match the accepted keys \'%s\'" % (str(set(payload.keys())),str(OS_PAYLOAD_PARAMETERS))
		flag= False
	else: 
		auth=payload["auth"]
		if set(auth.keys()) - OS_ACC_AUTH_PARAMETERS != set(): 
			m.reply = "The request auth field contains unaccepted parameters: \'%s\'" % str(set(auth.keys()) - OS_ACC_AUTH_PARAMETERS)
			flag= False
		elif OS_OBG_AUTH_PARAMETERS - set(auth.keys()) != set():
			m.reply = "The request auth field must contain the following parameters: \'%s\'" % str(OS_OBG_AUTH_PARAMETERS - set(auth.keys()))
			flag= False
	return flag,m

def verify_req_aws(payload):
	pass 
	# funtion to be implemented


