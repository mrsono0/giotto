from giotto.primitives import LOGGED_IN_USER
from giotto.exceptions import InvalidInput

def make_tables():
    from giotto import config
    Base = config.Base
    engine = config.engine
    Base.metadata.create_all(engine)
    return {'message': 'All tables created'}

def is_authenticated(message):
    """
    Is this request coming from a user who is logged in? This is a meta function.
    When adding this to a program, call it with the mesage you want to be displayed
    when no user is found.
    """
    def inner(user=LOGGED_IN_USER):
        if not user:
            raise InvalidInput(message)
        return {'user', user}
    return inner