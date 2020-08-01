import json

def readSuccessFile()-> dict:
	try:
		with open('ResponseMessage/SuccessMessage.json') as f:
			messages = json.load(f)
		return messages
	except Exception as e:
		raise e


def apiKeySuccessKey(api_key:str) -> dict:
	all_messages = readSuccessFile()
	api_success_message = all_messages['ApiKeySuccess']
	api_success_message['data']["ApiKey"] = api_key
	return api_success_message


def billAddedSuccess() -> dict :
	all_messages = readSuccessFile()
	return all_messages['AddBillSuccess']


def billFetchedSuccess() -> dict:
	all_messages = readSuccessFile()
	return all_messages['FetchBill']



def paymentUpdateSuccess() -> dict:
	all_messages = readSuccessFile()
	return all_messages['UpdatePayment']




