
import functools


def check_user_auth(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        while not self._logged_user:
            self.user_login()
        func(self, *args, **kwargs)
    return inner


class Controller:
    """Controlleur principal"""

    def __init__(self, repository, view):
        self.repository = repository
        self.view = view
        self._logged_user = None

    def start(self):
        self.welcome_page()
        self.user_info()

    def user_login(self):
        email, password = self.view.prompt_login()
        user = self.repository.user_login(email, password)
        if user:
            self._logged_user = user
            print("successfull")
        else:
            print(f"error {user}")

    def welcome_page(self):
        self.view.prompt_welcome_page()

    @check_user_auth
    def user_info(self):
        self.view.prompt_display_user_info(self._logged_user)
