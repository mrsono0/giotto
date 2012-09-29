class GiottoPrimitive(object): pass

class LOGGED_IN_USER(GiottoPrimitive):
	"""
	Represents the user logged in to the application.
	"""

class RAW_DATA(GiottoPrimitive):
	"""
	The raw load of data that came in from the user. Represented as a dict.
	"""

class USER_COUNTRY(GiottoPrimitive):
    """
    Represents the user's country based on GeoIP.
    """

class PREVIOUS_INPUT(GiottoPrimitive):
    pass

class PREVIOUS_ERRORS(GiottoPrimitive):
    pass