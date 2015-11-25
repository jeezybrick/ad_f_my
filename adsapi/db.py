import motor
from settings import DATABASE


class ConnectionHandler(object):
	"""
	Database connection handler.
	"""

	def __init__(self):
		"""
		Initializing the database setup.
		"""

		self.database, self.name = DATABASE['db_url'], DATABASE['name']

	def db_connect(self):
		"""
		Connecting mongodb server.
		"""

		client = motor.MotorClient(self.database).open_sync()
		self.db = client[self.name]
		return self.db

