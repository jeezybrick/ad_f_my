from django.contrib.auth.models import make_password
from publisher.models import Publisher
from sponsor.models import Sponsor

SESSION_KEY = '_auth_user_id'
USER_TYPE = '_user_type'

def authenticate(model, username, password):
	"""
	
	"""

	try:
		salted_password = make_password(password, salt="adfits")
		print salted_password
		user = model.objects.get(
			name=username, 
			password=salted_password
		)
		return user
	except:
		import sys
		print sys.exc_value
		return None

def login(request, user):
	if user is None:
		user = request.user
	
	if SESSION_KEY in request.session:
		if request.session[SESSION_KEY] != user.pk:
			# To avoid reusing another user's session, create a new, empty
			# session if the existing session corresponds to a different
			# authenticated user.
			request.session.flush()
	else:
		request.session.cycle_key()


def logout(request):
	"""
	"""

	request.session.flush()


	