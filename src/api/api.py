#/usr/bin/python3.10q
import connectors.openstack_conector as openstack
import fastapi
import api.cloud_gateway as cloud_gateway
from starlette.responses import FileResponse 
import api.db_gateway as db_gateway
app = fastapi.FastAPI()
import logging

@app.get("/",response_class=fastapi.responses.HTMLResponse)
async def root():
	return FileResponse('src/landing-page/index.html')

favicon_path = 'src/landing-page/AE.icon'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
	return FileResponse(favicon_path)

@app.post("/add_cloud")
async def add_cloud(info : fastapi.Request):
	logging.info("/addCloud is called")
	req = await info.json()
	logging.info("/addCloud request body: " + str(req))
	m = cloud_gateway.add_cloud(req)
	return m

@app.get("/get_servers")
async def get_servers(info : fastapi.Request):
	logging.info("/servers is called")
	req = await info.json()
	m=cloud_gateway.get_servers(req)
	return m

@app.get("/get_security_groups")
async def get_security_groups(info : fastapi.Request):
	logging.info("/get_security_groups is called")
	req = await info.json()
	m = cloud_gateway.get_security_groups(req)
	return m

@app.get("/update_security_groups")
async def update_security_groups(info : fastapi.Request):
	logging.info("/update_security_groups is called")
	req = await info.json()
	m = cloud_gateway.update_security_groups(req)
	return m

@app.get("/get_security_group")
async def get_security_group(info : fastapi.Request):
	logging.info("/get_security_group is called")
	req = await info.json()
	m = db_gateway.get_security_group(req)
	return m

@app.post("/create_security_group")
async def create_security_group(info : fastapi.Request):
	logging.info("/create_security_group is called")
	req = await info.json()
	m = cloud_gateway.create_security_group(req)
	return m

@app.post("/add_sg_rule")
async def add_sg_rule(info : fastapi.Request):
	logging.info("/add_sg_rule is called")
	req = await info.json()
	m = cloud_gateway.add_security_group_rule(req)
	return m

@app.post("/open_ip")
async def open_ip(info : fastapi.Request):
	logging.info("/open_ip is called")
	req = await info.json()
	m = cloud_gateway.open_ip(req)
	return m

@app.post("/add_kuberentes_token")
async def add_kuberentes_token(info : fastapi.Request):
	logging.info("/add_kuberentes_token is called")
	req = await info.json()
	m = db_gateway.add_kuberentes_token(req)
	return m

@app.get("/get_kuberentes_token")
async def get_kuberentes_token(info : fastapi.Request):
	logging.info("/get_kuberentes_token is called")
	req = await info.json()
	m = db_gateway.get_kuberentes_token(req)
	return m

@app.post("/create_db")
async def create_db(info : fastapi.Request):
	logging.info("/create DB is called")
	m = db_gateway.create_database()
	return m

@app.delete("/clear_db")
async def clear_db(info : fastapi.Request):
	logging.info("/clear DB is called")
	m = db_gateway.clear_database()
	return m