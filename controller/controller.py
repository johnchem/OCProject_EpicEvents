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
    def user_info(self, *args, **kwargs):
        self.view.prompt_user_info(self._logged_user)

    @check_user_auth
    def create_user(self, *args, **kwargs):
        if not self.permissions.create_user(self._logged_user):
            self.view.prompt_error_message("besoin d'un accés admin ou commercial pour cette opération")
            self.main_menu()
        data = self.view.prompt_create_user_form()
        user = models.User(**data)
        response = self.repository.add(user)

        if response:
            self.view.prompt_user_info(user)
            self.repository.commit()
            self.main_menu()

    @check_user_auth
    def list_user(self, *args, **kwargs):
        users = self.repository.list_user()
        choices = self.view.prompt_list_users(users)
        if choices == "q":
            self.main_menu()
        try:
            choices = int(choices)
            if choices > len(users):
                self.list_user()
            user_picked = users[choices-1]
            self.view.prompt_user_info(user_picked)
            self.user_opt_menu(user_picked)

        except Exception as err:
            self.view.print(err)
            self.view.prompt_error_message(
                (
                    f"Veuillez choisir une valeur entre 1 et {len(users)}"
                    + "\n ou q pour quitter"
                )
            )

    @check_user_auth
    def update_user(self, user, *args, **kwargs):
        if not self.permissions.update_user(self._logged_user):
            self.view.prompt_error_message("besoin d'un accés admin pour cette opération")
            self.user_opt_menu(user)

        # update_user_gen = self.repository.update_user(user.id)
        user_data = self.repository.get_user(user.email)
        user_data = self.view.prompt_display_update_user(user_data)

        # response = update_user_gen.send(user_data)
        response = self.repository.commit()
        if not response:
            self.view.prompt_error_message("erreur lors de la mise à jour")
        self.main_menu()

    @check_user_auth
    def delete_user(self, user_data, *args, **kwargs):
        response = self.repository.delete_user(user_data)
        if not response:
            self.view.prompt_error_message("erreur lors de la suppression")
        self.view.print("L'utilisateur à bien été supprimé")
        self.main_menu()

    @check_user_auth
    def create_client(self):
        if self.permissions.create_client(self._logged_user):
            default_commercial = self._logged_user
            data = self.view.prompt_create_client(default_commercial.email)

            if data["commercial_contact"] != default_commercial.email:
                data["commercial_contact"] = self.repository.get_user(data.commercial_contact)
            else:
                data["commercial_contact"] = default_commercial

            client = models.Client(**data)
            response = self.repository.add(client)
        if response:
            self.repository.commit()
            self.view.prompt_client_info(client)
            self.main_menu()

    @check_user_auth
    def list_client(self):
        client = self.repository.list_client()
        choices = self.view.prompt_list_client(client)
        if choices == "q":
            self.main_menu()
        try:
            choices = int(choices)
            if choices > len(client):
                self.list_user
            client_picked = client[choices-1]
            self.view.prompt_client_info(client_picked)
            self.client_opt_menu(client_picked)

        except Exception as err:
            self.view.print(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(client)}",
                "ou q pour quitter",
            )

    @check_user_auth
    def update_client(self, client, *args, **kwargs):
        if not self.permissions.update_client(self._logged_user):
            self.view.prompt_error_message("besoin d'un accés admin pour cette opération")
            self.client_opt_menu(client)

        client_data = self.view.prompt_update_client(
            client,
            commercial_email=client.commercial.email)
        client_data["commercial"] = self.repository.get_user(client_data.email)

        # response = update_user_gen.send(user_data)
        response = self.repository.commit()
        if not response:
            self.view.prompt_error_message("erreur lors de la mise à jour")
        self.main_menu()

    @check_user_auth
    def delete_client(self):
        pass

    @check_user_auth
    def create_contract(self, *args, **kwargs):
        if self.permissions.create_contract(self._logged_user):
            if "client" in kwargs:
                client = kwargs.get("client")

                data = self.view.prompt_create_contract(
                    client=client,
                    )
                data["client"] = client
            else:
                data = self.view.prompt_create_contract()
                data["client"] = self.repository.get_client(data["client"])

            contrat = models.Contrat(**data)
            response = self.repository.add(contrat)
        if response:
            self.repository.commit()
            self.view.prompt_contract_info(contrat)
            self.main_menu()

    @check_user_auth
    def list_contract(self):
        pass

    @check_user_auth
    def filter_contract(self):
        pass

    @check_user_auth
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
