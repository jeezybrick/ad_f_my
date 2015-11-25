import os

DEBUG = False

PROJECT_BASE = os.path.dirname(os.path.dirname(__file__))
STATIC_PATH = os.path.join(PROJECT_BASE, "static/ads")

if DEBUG:
	MEDIA_URL = "http://localhost:8000/media/"
	REDIRECT_URl = "http://192.168.10.170:8000/"
	DB_URL = 'mongodb://admin:mindfire@localhost:27017'
else:
	MEDIA_URL = "http://23.239.11.140/media/"
	REDIRECT_URl = "http://23.239.11.140"
	DB_URL = 'mongodb://adf-admin:$AF*99!*Al!2014#$@localhost:27017'

DATABASE = {
	'db_url': DB_URL,
	'name': 'adfits'
}

PER_COUPON_DOLLAR = 5

MANDRILL_API_KEY = "hUOpJAHnhJGoZhFzKeWLog"
REDEEM_SUBJECT = "You have earned a new reward"
REDEEM_MESSAGE = '''
<pre>
Dear Collector

SUPERB!

Thank you for your loyalty to %s. We appreciate readers like you!

By visiting us daily, you have successfully redeemed a $5 Gift Card from %s.

A separate email will sent with all your reward details. Please allow up to 72 hours to receive your reward.

Thanks again and we hope you enjoy your gift!

Sincerely,

Jennifer Williams

@ADfits
</pre>
'''