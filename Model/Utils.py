from datetime import datetime
from random import randint


def getApiKeyId():
	dt = datetime.now()
	seq = int(dt.strftime("%Y%m%d%H%M%S"))
	rand_ = ''.join(["{}".format(randint(0, 9)) for num in range(0, 4)])
	token_id = "KeyId-" + str(seq) + str(rand_)
	return token_id


def getBillId():
	dt = datetime.now()
	seq = int(dt.strftime("%Y%m%d%H%M%S"))
	rand_ = ''.join(["{}".format(randint(0, 9)) for num in range(0, 4)])
	bill_id = "BillId-" + str(seq) + str(rand_)
	return bill_id

def getTransactionId():
	dt = datetime.now()
	seq = int(dt.strftime("%Y%m%d%H%M%S"))
	rand_ = ''.join(["{}".format(randint(0, 9)) for num in range(0, 4)])
	transaction_id = "TransactionId-" + str(seq) + str(rand_)
	return transaction_id

def getAckId():
	rand_ = ''.join(["{}".format(randint(0, 9)) for num in range(0, 5)])
	ack_id = "AX0"+str(rand_)
	return ack_id


def generateApiKeySchema(api_key: str) -> dict:
	schema = {}
	schema['ApiKey'] = api_key
	dt = datetime.now()
	date_ = dt.isoformat()
	schema['GenerateTime'] = date_
	schema['Status'] = "Alive"
	return schema


def checkLife(reg_time: str) -> bool:
	''' Check the time is 24 hours old or not '''
	reg_time_ = datetime.fromisoformat(reg_time)
	time_diff = datetime.now() - reg_time_
	hours = divmod(time_diff.total_seconds(), 3600)[0]

	if hours < 24:
		return True
	else:
		return False