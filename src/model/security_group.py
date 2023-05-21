import logging
from src.model.security_group_rule import SGR

class SG:
	def __init__(self, item, cloud_name):
		self.name = item["name"]
		self.id = item["id"]
		self.description = item["description"]
		self.rules=self._create_rules(item["security_group_rules"], cloud_name)
		self.created_at = item["created_at"]
		self.revision_number = item["revision_number"]
		self.provider = cloud_name

	def _create_rules(self, json_rules, cloud_name):
		rules = []
		for json_rule in json_rules: 
			rule = SGR(json_rule, self.name, cloud_name)
			rules.append(rule)
		return rules

	def __str__(self) -> str:
		output = f"{self.name} : id \"{self.id}\" Provider: \"{self.provider}\": \n"
		if self.rules: 
			output += f"\t rules: \n"
			for rule in self.rules:
				output += "\t\t" + rule.__str__() + "\n"
		return output

	def to_dict(self) -> dict: 
		d=self.__dict__
		d["rules"]=[rule.__dict__ for rule in self.rules]
		return d
	
	@staticmethod
	def from_dict(): 
		pass
