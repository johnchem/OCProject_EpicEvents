import functools


def login(function):
    @functools.wraps(function)
    def inner(self, *args, **kwargs):
        while not self._logged_user:
            self.user_login()
        function(self, *args, **kwargs)

    return inner


def visitor_allowed(function):
    """Tag a method so that it shouldn't be decorated to call self.load."""
    function.request_login = False
    return function


def login_required(function):
    try:
        return bool(function.visitor_allowed)
    except AttributeError:
        return False
