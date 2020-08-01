import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from Model.DBConfig import *
from Model.Utils import *



def getConnection():
	cred = credentials.Certificate(getCredLocation())
	firebase_admin.initialize_app(cred, {
		'databaseURL': getDbUrl()
	})
	app = firebase_admin.get_app()
	ref = db.reference('/')
	return ref, app

def endConnection(app):
	firebase_admin.delete_app(app)


def saveApiKey(api_key: str) -> bool:
	try:
		api_key_id = getApiKeyId()
		api_key_schema = generateApiKeySchema(api_key)
		ref, app = getConnection()

		api_key_ref = ref.child('APIKEYS')
		save_key = api_key_ref.child(api_key_id)
		save_key.set(api_key_schema)
		endConnection(app)
		return api_key_schema["ApiKey"]
	except Exception as e:
		return False


def checkApiKey(auth: str) -> dict:
	ref, app = getConnection()	
	access_token_ref = ref.child('APIKEYS')
	all_val = access_token_ref.order_by_key().get()
	all_val_ = dict(all_val)
	check = [v for key, v in all_val_.items() if v['ApiKey'] == auth]
	endConnection(app)
	if check:
		val = check[0]
		reg_time = val['GenerateTime']
		check_life = checkLife(reg_time)
		if check_life:
			return {"status": True}
		else:
			return {"status": False, "value": "Key is expired"}
	else:
		return {"status": False, "value": "Invalid key"}


def chechBillAdded(mobile_number:str) -> bool:
	''' Check the number is already added or not '''
	ref, app = getConnection()
	bill_ref = ref.child('BILL')
	all_val = bill_ref.order_by_key().get()
	all_val_ = dict(all_val)
	endConnection(app)
	check = [v for key, v in all_val_.items() if v['mobileNumber'] == mobile_number]
	if check:
		return True
	else:
		return False


def checkReqIdAdded(req_id:str) -> bool:
	''' Check the number is already added or not '''
	ref, app = getConnection()
	bill_ref = ref.child('BILL')
	all_val = bill_ref.order_by_key().get()
	all_val_ = dict(all_val)
	endConnection(app)

	check = [v for key, v in all_val_.items() if v['refID'] == req_id]
	if check:
		return True
	else:
		return False


def saveBill(data: dict):
	try:
		is_number_added = chechBillAdded(data['mobileNumber'])
		is_reqid_added = checkReqIdAdded(data['refID'])
		if is_number_added:
			return {"status": False,"message": "number-already-exists"}
		if is_reqid_added:
			return {"status": False,"message": "reqid-already-exists"}
		
		bill_id = getBillId()
		ref, app = getConnection()
		bill_ref = ref.child('BILL')
		save_bill = bill_ref.child(bill_id)
		save_bill.set(data)
		endConnection(app)
		return {"status":True, "message": "added"}
	except Exception as e:
		return {"status": False,"message": "bill-not-added"}


def getBill(data: dict) -> dict:
	try:
		ref, app = getConnection()
		bill_ref = ref.child('BILL')
		all_val = bill_ref.order_by_key().get()
		all_val_ = dict(all_val)
		endConnection(app)
		check = [v for key, v in all_val_.items() if v['mobileNumber'] == str(data['mobileNumber'])]
		if check:
			return {"status":True, "message": check[0]}
		else:
			return {"status":False, "message": "customer-not-found"}

	except Exception as e:
		return {"status":False, "message": "unhandled-error"}


def getDueAmount(refID):
	ref, app = getConnection()
	bill_ref = ref.child('BILL')
	all_val = bill_ref.order_by_key().get()
	all_val_ = dict(all_val)
	endConnection(app)
	check = [v for key, v in all_val_.items() if v['refID'] == refID]

	return check[0]['dueAmount']


def checkAmount(amount:str, refID: str) -> bool:
	''' Check amount is not negetive and not other string '''
	try:
		amount_float = float(amount)
		if amount_float>0:
			due_amount = getDueAmount(refID)
			due_amount_ = float(due_amount)
			if float(amount) > due_amount_:
				return False
			else:
				return True
		else:
			return False
	except:
		return False


def updateAmount(refID: str, amount: str) -> str :
	due_amount = float(getDueAmount(refID))
	updated_amount = due_amount - float(amount)
	return updated_amount


def updateDb(refID, update_amount):
	try:
		ref, app = getConnection()
		bill_ref = ref.child('BILL')
		all_val = bill_ref.order_by_key().get()
		all_val_ = dict(all_val)
		val = ''
		key = ''
		for k, v in all_val_.items():
			if v['refID'] == refID:
				key = k
				val = v
				amount = float(v['dueAmount'])
				break
		val['dueAmount'] = str(update_amount)
		newVal = {}
		newVal[key] = val
		bill_ref.update(newVal)
		endConnection(app)
		return True
	except:
		return False

def updateTransaction(transaction: dict) -> bool:
	try:
		transaction_id = getTransactionId()
		ref, app = getConnection()
		transaction_ref = ref.child('TRANSACTION')
		save_transaction = transaction_ref.child(transaction_id)
		ack_id = getAckId()
		transaction["ackId"] = ack_id
		save_transaction.set(transaction)
		endConnection(app)
		return ack_id
	except:
		return False


def updateBill(data:dict) -> dict:
	is_reqid_added = checkReqIdAdded(data['refID'])
	if is_reqid_added:
		check_amount = checkAmount(data['transaction']['amountPaid'], data['refID'])
		if check_amount:
			update_amount = updateAmount(data['refID'], data['transaction']['amountPaid'])
			update_data = updateDb(data['refID'], update_amount)
			if update_data:
				update_transaction = updateTransaction(data)
				
				if update_transaction:
					resposne_data = {"ackId":update_transaction}
					return {"status": True,"message":resposne_data}
				else:
					return {"status":False, "message": "unhandled-error"}

			else:
				return {"status":False, "message": "unhandled-error"}
		else:
			return {"status": False,"message":"amount-mismatch"}
	else:
		return {"status": False,"message":"invalid-ref-id"}

	