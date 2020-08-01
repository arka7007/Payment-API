import yaml


def getAuthKey():
	try:
		with open(r'Configuration/Key.yaml') as file:
			configuration = yaml.load(file, Loader=yaml.FullLoader)
			key = configuration['PublicKey']
		return key
	except Exception as e:
		raise e
	