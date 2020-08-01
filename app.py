from flask import Flask, jsonify, request 
import json
from Service import *
from ResponseMessage.ErrorMessage import *
from ResponseMessage.SuccessMessage import *


app = Flask(__name__)


@app.route('/api/v1/get-token', methods=['POST'])
def getToken():
	if request.method == 'POST':
		data = request.get_json()

		if data is None:
			return jsonify(parametersError())

		check_params = checkAuthKeyRequestParams(data)

		if check_params:
			check_keys = checkAccessKeyRequestKeys(data['AccessKey'])
			if check_keys:
				api_key = getApiKey()
				if api_key:
					return jsonify(apiKeySuccessKey(api_key))
				else:
					return jsonify(unhandledError())
			else:
				return jsonify(authEror())
		else:
			return jsonify(parametersError())


@app.route('/api/v1/add-bill', methods=['POST'])
def addUser():
	if request.method == 'POST':
		headers = request.headers
		auth = headers.get("X-Api-Key")
		is_auth_valid = validateApiKey(auth)

		if is_auth_valid['status']:
			data = request.get_json()
			if data is None:
				return jsonify(parametersError())
			check_params = checkAddBillParams(data)

			if check_params:
				check_data_type = checkAddBillDataTye(data)
				if check_data_type:
					is_added = addBill(data)
					if is_added['status']:
						return jsonify(billAddedSuccess())
					else:
						error_message = unhandledError()
						error_message['errorMessage'] = is_added['message']
						return jsonify(error_message)
				else:
					error_message = parametersError()
					error_message['errorMessage'] = 'invalid-data-type'
					return jsonify(error_message)
			else:
				return jsonify(parametersError())
		else:
			error_message = authEror()
			error_message['errorMessage'] = is_auth_valid['value']
			return jsonify(error_message)


@app.route('/api/v1/fetch-bill', methods = ['POST'])
def fetchBill():
	if request.method == 'POST':
		headers = request.headers
		auth = headers.get("X-Api-Key")
		is_auth_valid = validateApiKey(auth)
		if is_auth_valid['status']:
			data = request.get_json()
			if data is None:
				return jsonify(parametersError())
			check_params = chceckFetchBillRequestParams(data)
			if check_params:
				fetch_bill = getBillDetails(data)

				if fetch_bill['status']:
					success_message = billFetchedSuccess()
					success_message['data'] = fetch_bill['message']
					return jsonify(success_message)
				else:
					if fetch_bill['message'] == 'customer-not-found':
						return jsonify(customerNotFoundError())
					else:
						return jsonify(unhandledError())
			else:
				return jsonify(parametersError())
		else:
			error_message = authEror()
			error_message['errorMessage'] = is_auth_valid['value']
			return jsonify(error_message)


@app.route('/api/v1/payment-update', methods = ['POST'])
def paymentUpdate():
	if request.method == 'POST':
		headers = request.headers
		auth = headers.get("X-Api-Key")
		is_auth_valid = validateApiKey(auth)
		if is_auth_valid['status']:
			data = request.get_json()
			if data is None:
				return jsonify(parametersError())
			check_params = chceckUpdateBillRequestParams(data)
			if check_params:
				is_updated = updatePayment(data)

				if is_updated['status']:
					data_to_send = is_updated['message']
					success_message = paymentUpdateSuccess()
					success_message['data'] = data_to_send
					return jsonify(success_message)
				else:
					if is_updated['message'] == "invalid-ref-id":
						return jsonify(invalidRefIdError())
					if is_updated['message'] == "amount-mismatch":
						return jsonify(amountMismatchError())
					if is_updated['message'] == "unhandled-error":
						return jsonify(unhandledError())
			else:
				return jsonify(parametersError())

		else:
			error_message = authEror()
			error_message['errorMessage'] = is_auth_valid['value']
			return jsonify(error_message)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080,debug=True)