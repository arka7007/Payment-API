from random import randint
from datetime import datetime


def generateApiKey():
	dt = datetime.now()
	seq = int(dt.strftime("%Y%m%d%H%M%S"))
	rand_ = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
	api_key = "key-" + str(seq) + str(rand_)
	return api_key