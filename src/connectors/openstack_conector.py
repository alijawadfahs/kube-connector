import openstack
import yaml
import src.database.db as database
from src.model.server import Server
from src.model.security_group import SG
import logging

def get_servers(cloud_name): 
	openstack.enable_logging(debug=True, path='openstack.log')
	# Initialize connection
	conn = openstack.connect(cloud=cloud_name)
	l=[server.to_dict() for server in conn.compute.servers()]
	servers=[]
	for item in l:
		server = Server(item,cloud_name,"openstack")
		servers.append(server)
	return servers

def get_security_groups(cloud_name):
	openstack.enable_logging(debug=True, path='openstack.log')
	# Initialize connection
	conn = openstack.connect(cloud=cloud_name)
	security_groups = []
	json_security_groups=conn.network.security_groups()
	for json_security_group in json_security_groups: 
		security_group=SG(json_security_group, cloud_name, "openstack")
		security_groups.append(security_group)
	return security_groups

def create_security_group(cloud_name,sg_name):
	openstack.enable_logging(debug=True, path='openstack.log')
	conn = openstack.connect(cloud=cloud_name)
	security_group = conn.network.create_security_group(name = sg_name, description = "Kube-connector generated security group" )
	return security_group

def open_ip(cloud_name,sg_id,ip):
	port={
		"direction" : "ingress",
		"ip" : f"{ip}/32",
		"protocol" : "tcp",
		"port_range_max" : 65534,
		"port_range_min" : 1,
		"ethertype" : "IPv4"
	}
	added_rules=[]
	added_rules.append(open_port(cloud_name,sg_id,port))

	port["protocol"] = "udp"
	added_rules.append(open_port(cloud_name,sg_id,port))
	port["protocol"] = "icmp"
	port["port_range_max"] = None
	port["port_range_min"] = None
	added_rules.append(open_port(cloud_name,sg_id,port))
	return added_rules
	

def open_port(cloud_name,sg_id,port):
	openstack.enable_logging(debug=True, path='openstack.log')
	conn = openstack.connect(cloud=cloud_name)
	added_rule = conn.network.create_security_group_rule(
		security_group_id	= sg_id,
		direction			= port["direction"],
		remote_ip_prefix	= port["ip"],
		protocol			= port["protocol"],
		port_range_max		= port["port_range_max"],
		port_range_min		= port["port_range_min"],
		ethertype			= port["ethertype"])
	return added_rule

def create_openstack_yaml(name,req):
	d={"clouds": {name:req}}
	with open(r'./clouds.yaml', 'w') as file:
		documents = yaml.dump(d, file)


	