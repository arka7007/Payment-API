import json

def readErrorFile():
	try:
		with open('ResponseMessage/ErrorMessage.json') as f:
			messages = json.load(f)
		return messages
	except Exception as e:
		raise e
	

def authEror() -> dict:
	''' Return Error Message for Auth key '''
	messages = readErrorFile()
	return messages['auth_error']
	

def parametersError() -> dict:
	''' Return error Message for Parameters '''
	messages = readErrorFile()
	return messages['param_error']


def customerNotFoundError() -> dict:
	''' Return error Message if Customer not Found '''
	messages = readErrorFile()
	return messages['customer_not_found_error']


def invalidRefIdError() -> dict:
	''' Return error Message if Customer not Found '''
	messages = readErrorFile()
	return messages['invalid_ref_id_error']


def amountMismatchError() -> dict:
	''' Return error Message if Customer not Found '''
	messages = readErrorFile()
	return messages['amount_mismatch_error']


def pathNotFoundError() -> dict:
	''' Return error Message if Customer not Found '''
	messages = readErrorFile()
	return messages['path_not_found_error']


def unhandledError() -> dict:
	''' Return error Message if Customer not Found '''
	messages = readErrorFile()
	return messages['unhandled_error']


