import logging

class SGR:
	def __init__(self, item, sg_name, cloud_name):
		self.id = item["id"]
		self.ethertype = item["ethertype"]
		self.port_range_min = item["port_range_min"]
		self.port_range_max = item["port_range_max"]
		self.protocol = item["protocol"]
		self.remote_ip_prefix = item["remote_ip_prefix"]
		self.created_at = item["created_at"]
		self.parent_name = sg_name
		self.parent_id = item["security_group_id"]
		self.provider = cloud_name
		
	def __str__(self) -> str:
		return f"{self.id} : Source \"{self.remote_ip_prefix}\" Range: \"{self.port_range_min}:{self.port_range_max}\" Protocol: \"{self.protocol}\""
	
	@staticmethod
	def from_dict(): 
		pass