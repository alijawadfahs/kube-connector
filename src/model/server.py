import logging

class Server: 
	def __init__(self,item, cloud_name, provider_type):
		self.name = item["name"]
		self.id = item["id"]
		self.provider_type = provider_type
		self.provider_name = cloud_name 
		self.region = item["location"]["region_name"]
		self.status = item["status"]
		self.type = item["flavor"]["id"]
		self.launched = item["launched_at"]
		self._get_ipv4(item["addresses"])
		self._get_security_groups(item["security_groups"])

	def _get_ipv4(self, addresses): 
		for l in addresses.values():
			for address in l:
				if address["version"] == 4: 
					self.address = address["addr"]
					return
		logging.warn("No IPV4 address was found for the server \"%s\" with id \"%s\"" % (self.name,self.id))
		self.address = "n/a"

	def _get_security_groups(self, security_groups):
		temp_security_groups=[]
		if not len(security_groups): 
			logging.warn("No security group was found for the server \"%s\" with id \"%s\"" % (self.name,self.id))
		for d in security_groups: 
			temp_security_groups.append(d["name"])
		self.security_groups=temp_security_groups