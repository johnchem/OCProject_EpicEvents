import functools
import backend.models as models
import controller.menu as menu


def check_user_auth(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        while not self._logged_user:
            self.user_login()
        func(self, *args, **kwargs)
    return inner


class Controller(menu.Menu):
    """Controlleur principal"""

    def __init__(self, repository, view, permissions):
        menu.Menu.__init__(self, view)
        self.repository = repository
        self.permissions = permissions
        self._logged_user = None

    def start(self):
        self.welcome_page()
        if not self._logged_user:
            self.user_login
        self.user_info()
        self.main_menu()

    def welcome_page(self):
        self.view.prompt_welcome_page()

    def user_login(self):
        email, password = self.view.prompt_login()
        user = self.repository.user_login(email, password)
        if user:
            self._logged_user = user
            print("successfull")
        else:
            print(f"error {user}")

    @check_user_auth
    def user_info(self):
        self.view.prompt_display_user_info(self._logged_user)

    @check_user_auth
    def create_user(self):
        if self.permissions.create_user(self._logged_user):
            data = self.view.prompt_create_user_form()
            user = models.User(**data)
            response = self.repository.add(user)
        if response:
            self.view.prompt_display_user_info(user)
            self.main_menu()

    @check_user_auth
    def list_user(self):
        users = self.repository.list_user()
        choices = self.view.prompt_list_users(users)
        if choices == "q":
            self.main_menu()
        try:
            choices = int(choices)
            if choices > len(users):
                self.list_user
            user_picked = users[int(choices)]
            self.view.prompt_display_user_info(user_picked)
        except:
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(choices)}",
                "ou q pour quitter",
            )

    def update_user(self, user_id):
        if not self.permissions.update_user(self._logged_user):
            self.view.prompt_error_message("besoin d'un accés admin pour cette opération")
        user_data = self.repository.update_user(user_id)
        self.view.prompt_display_update_user(user_data)
        response = next(user_data)
        if not response:
            self.view.prompt_error_message("erreur lors de la mise à jour")    
        self.main_menu()

    def delete_user(self, user_id):
        response = self.repository.delete_user(user_id)
        if not response:
            self.view.prompt_error_message("erreur lors de la suppression")    
        self.main_menu()

    def create_client(self):
        if self.permissions.create_client(self._logged_user):
            default_commercial = self._logged_user
            data = self.view.prompt_create_client_form(default_commercial)
            client = models.Client(**data)
            response = self.repository.add(client)
        if response:
            self.view.prompt_display_client_info(client)
            self.main_menu()

    def list_client(self):
        client = self.repository.list_client()
        choices = self.view.prompt_list_users(client)
        if choices == "q":
            self.main_menu()
        try:
            choices = int(choices)
            if choices > len(client):
                self.list_user
            user_picked = client[int(choices)]
            self.view.prompt_display_client_info(user_picked)
        except:
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(choices)}",
                "ou q pour quitter",
            )

    def update_client(self):
        pass

    def delete_client(self):
        pass

    def create_contract(self):
        pass

    def list_contract(self):
        pass

    def filter_contract(self):
        pass

    def update_contract(self):
        pass

    def delete_contract(self):
        pass

    def create_event(self):
        pass

    def list_events(self):
        pass

    def filter_events(self):
        pass

    def update_event(self):
        pass

    def delete_event(self):
        pass

    def quit(self):
        # self.view.exit_message()
        exit()


if __name__ == "__main__":
    pass
