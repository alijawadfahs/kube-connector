from tinydb import TinyDB, Query
import os
DIR="./DB/Store"
FILES=["Clouds.json", "Tokens.json", "IPs.json", "Servers.json", "Security_Groups.json"]
import logging

def create_database():
	create_dir()
	clouds          =   load_clouds()
	servers         =   load_servers()
	tokens          =   load_tokens()
	# ips             =   load_public_ips()
	security_groups =   load_security_groups()

def create_dir():
	isExist = os.path.exists(DIR)
	if not isExist:
		os.makedirs(DIR)
		logging.info("Created the DIR: "+ DIR)

def load_clouds(file=DIR+"/Clouds.json"):
	db = TinyDB(file)
	logging.info("Loaded clouds table")
	return db 

def load_servers(file=DIR+"/Servers.json"): 
	db = TinyDB(file)
	logging.info("Loaded servers table")
	return db

def load_security_groups(file=DIR+"/Security_Groups.json"): 
	db = TinyDB(file)
	logging.info("Loaded servers table")
	return db

def load_tokens(file=DIR+"/Tokens.json"): 
	db = TinyDB(file)
	logging.info("Loaded tokens table")
	return db 

# def load_public_ips(file=DIR+"/IPs.json"):
# 	logging.info("Loaded ips table") 
# 	db = TinyDB(file)
# 	return db

def add_cloud_item(cloud_item): 
	cloud=load_clouds()
	cloud_table=cloud.table("Clouds")
	out=cloud_table.insert(cloud_item)
	return out

def add_server_item(server_item):
	servers=load_servers()
	servers_table=servers.table("Servers")
	out=servers_table.insert(server_item)
	return out

def add_sg_item(sg_item):
	security_groups=load_security_groups()
	security_groups_table=security_groups.table("Security_Groups")
	out=security_groups_table.insert(sg_item)
	return out

def get_sg_ids():
	security_groups=load_security_groups()
	security_groups_table=security_groups.table("Security_Groups")
	out=[sg["id"] for sg in security_groups_table.all()]
	return out

def add_kubernetes_token(token):
	tokens=load_tokens()
	tokens_table=tokens.table("Tokens")
	out = tokens_table.insert({"token" : token})
	return out

def get_security_group(sg_name): 
	security_groups=load_security_groups()
	security_groups_table=security_groups.table("Security_Groups")
	query = Query()
	return security_groups_table.search(query.name == sg_name)

def get_kubernetes_token(token_id): 
	kubernetes_tokens=load_tokens()
	kubernetes_tokens_table=kubernetes_tokens.table("Tokens")
	return kubernetes_tokens_table.get(doc_id=token_id)

def clear_database(): 
	for file in FILES:
		to_be_deleted= f"{DIR}/{file}"
		if os.path.exists(to_be_deleted):
			os.remove(to_be_deleted)
