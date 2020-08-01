from Configuration.Config import *
from Utils import *
from RequestKeys.RequestParams import *
from Model.model import *


def checkAuthKeyRequestParams(data: dict) -> bool:
	''' Check requests params are there'''
	if list(set(getAuthKeyRequestsParams()) - set(list(data.keys()))):
		return False
	else:
		return True


def checkAccessKeyRequestKeys(auth_key: str) -> bool:
	''' Validate Auth key '''
	key = getAuthKey()
	if key == auth_key:
		return True
	else:
		return False


def getApiKey() -> str or bool:
	''' Generating API key and save to data base '''
	api_key = generateApiKey()
	save_api_key = saveApiKey(api_key)
	if save_api_key:
		return save_api_key
	else:
		return False


def validateApiKey(auth: str) -> dict:
	''' Validate the Api key '''
	check_auth = checkApiKey(auth)
	return check_auth


def checkAddBillParams(data:dict) -> bool:
	''' Check requests params are there '''
	if list(set(getAddBillParams()) - set(list(data.keys()))):
		return False
	else:
		return True


def checkAddBillDataTye(data: dict) -> bool:
	''' Check data type of request json '''
	check = {}
	check['name'] = isinstance(data['customerName'], str)
	check['dueDate'] = isinstance(data['dueDate'], str)
	try:
		check['dueAmount'] = float(data['dueAmount'])
		if check['dueAmount']>0:
			check['dueAmount'] = True
		else:
			check['dueAmount'] = False
	except:
		check['dueAmount'] = False

	try:
		check['mobileNumber'] = int(data['mobileNumber'])
		if check['mobileNumber']>0:
			check['mobileNumber'] = True
		else:
			check['mobileNumber'] = False
	except:
		check['mobileNumber'] = False
	validate = [k for k, v in check.items() if v == False]
	if len(validate)>0 and validate:
	    return False
	else:
	    return True


def addBill(data:dict) -> bool:
	''' Save bill to database '''
	is_added = saveBill(data)
	return is_added


def chceckFetchBillRequestParams(data: dict) -> bool:
	''' Check requests params are there '''
	if list(set(getFetchBillParams()) - set(list(data.keys()))):
		return False
	else:
		return True


def getBillDetails(data: dict) -> dict:
	''' Fetch bill details '''
	bill_details = getBill(data)
	return bill_details


def chceckUpdateBillRequestParams(data: dict) -> bool:
	''' Check request params are there '''
	if list(set(getUpdatePaymentarams()) - set(list(data.keys()))):
		return False
	else:
		data_ = data['transaction']
		print("transaction :  ", data_)
		if list(set(getTransactionParams()) - set(list(data_.keys()))):
			return False
		else:
			return True


def updatePayment(data: dict) -> dict:
	''' Update bill '''
	is_updated = updateBill(data)
	return is_updated






