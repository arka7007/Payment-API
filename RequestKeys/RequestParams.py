import json


def readKeyFile():
	try:
		with open('RequestKeys/Keys.json') as f:
			all_keys = json.load(f)
		return all_keys
	except Exception as e:
		raise e

def getAuthKeyRequestsParams():
	all_keys = readKeyFile()
	return all_keys['AuthRequestKey']

def getAddBillParams():
	all_keys = readKeyFile()
	return all_keys['AddBillKeys']


def getFetchBillParams():
	all_keys = readKeyFile()
	return all_keys['FetchBillKeys']


def getUpdatePaymentarams():
	all_keys = readKeyFile()
	return all_keys['UpdatePaymentKeys']


def getTransactionParams():
	all_keys = readKeyFile()
	return all_keys['TransactionKeys']
