import yaml

def parseConfigFile():
	with open(r'Model/DbConfig.yaml') as file:
		configuration = yaml.load(file, Loader=yaml.FullLoader)
	return configuration


def getCredLocation():
	config = parseConfigFile()
	return config['CredKeyLocation']


def getDbUrl():
	config = parseConfigFile()
	return config['DataBaseUrl']