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
        if not self.permissions.delete_user(self._logged_user):
            self.view.prompt_error_message(
                "besoin d'un accés admin ou faire partis \n de l'équipe gestion pour cette opération")
            self.user_opt_menu(user_data)
        response = self.repository.delete_user(user_data)
        if not response:
            self.view.prompt_error_message("erreur lors de la suppression")
        self.view.print("L'utilisateur à bien été supprimé")
        self.main_menu()

    @check_user_auth
    def create_client(self):
        if not self.permissions.create_client(self._logged_user):
            self.view.prompt_error_message(
                "besoin d'un accés admin ou faire partis \n de l'équipe gestion pour cette opération")
            self.user_menu()
        else:
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
        if not self.permissions.read_client(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.user_menu()

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
    def update_client(self, client):
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
    def delete_client(self, client):
        if not self.permissions.delete_client(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.client_opt_menu(client)

        response = self.repository.delete_user(client)
        if not response:
            self.view.prompt_error_message("erreur lors de la suppression")
        self.view.print("Le client à bien été supprimé")
        self.client_menu()

    @check_user_auth
    def create_contract(self, client=None):
        if not self.permissions.create_contract(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.client_menu()

        if client:
            if not self.permissions.create_contract(self._logged_user):
                self.view.prompt_error_message("besoin d'un accés admin pour cette opération")
                self.client_opt_menu(client)

            data = self.view.prompt_create_contract(
                client=client,
            )
            data["client"] = client
        else:
            if not self.permissions.create_contract(self._logged_user):
                self.view.prompt_error_message("besoin d'un accés admin pour cette opération")
                self.contract_menu()

            data = self.view.prompt_create_contract()
            data["client"] = self.repository.get_client(data["client"])

        contrat = models.Contrat(**data)
        response = self.repository.add(contrat)

        if response:
            self.repository.commit()
            self.view.prompt_contract_info(contrat)
            self.contract_menu()

    @check_user_auth
    def list_contract(self):
        if not self.permissions.read_contract(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.contract_menu()
        contract = self.repository.list_contract()
        choices = self.view.prompt_list_contract(contract)
        if choices == "q":
            self.contract_menu()
        try:
            choices = int(choices)
            if choices > len(contract):
                self.list_user
            contract_picked = contract[choices-1]
            self.view.prompt_contract_info(contract_picked)
            self.contract_opt_menu(contract_picked)

        except Exception as err:
            self.view.print(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(contract)}",
                "ou q pour quitter",
            )

    @check_user_auth
    def filter_contract(self):
        pass

    @check_user_auth
    def update_contract(self, contract):
        if not self.permissions.update_contract(self._logged_user, contract):
            self.view.prompt_error_message("accés non authorisé")
            self.contract_opt_menu(contract)
        contract_data = self.view.prompt_update_contract(
            contract,
            client_fullname=contract.client.full_name,
            commercial_email=contract.commercial.email,
            )
        contract_data["commercial"] = self.repository.get_user(contract_data["commercial_email"])
        contract_data["client"] = self.repository.get_client(contract_data["client_fullname"])

        # response = update_user_gen.send(user_data)
        response = self.repository.commit()
        if not response:
            self.view.prompt_error_message("erreur lors de la mise à jour")
        self.main_menu()

    def delete_contract(self, contract):
        if not self.permissions.delete_contract(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.contract_opt_menu(contract)

        response = self.repository.delete_contract(contract)
        if not response:
            self.view.prompt_error_message("erreur lors de la suppression")
        self.view.print("Le contrat à bien été supprimé")
        self.contract_menu()

    def create_event(self, contract):
        if not self.permissions.update_contract(self._logged_user, contract):
            self.view.prompt_error_message("accés non authorisé")
            self.contract_opt_menu(contract)
        if contract.contrat_status == models.ContratStatus.SIGNED:
            event_data = self.view.prompt_create_event(
                contract=contract
            )
            event_data["client"] = contract.client
            event = models.Evenement(**event_data)
            response = self.repository.add(event)

            if response:
                self.repository.commit()
                self.view.prompt_event_info(event)
                self.contract_opt_menu(contract)
            else:
                self.view.prompt_error_message("erreur lors de la creation")
                self.contract_opt_menu(contract)
        else:
            self.view.prompt_error_message("Le contrat doit être signé pour crée un évenement")
            self.contract_opt_menu(contract)

    def list_events(self):
        if not self.permissions.read_event(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.event_menu()

        event = self.repository.list_event()
        choices = self.view.prompt_list_event(event)
        if choices == "q":
            self.contract_menu()
        try:
            choices = int(choices)
            if choices > len(event):
                self.list_user
            event_picked = event[choices-1]
            self.view.prompt_event_info(event_picked)
            self.event_opt_menu(event_picked)

        except Exception as err:
            self.view.print(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(event)}",
                "ou q pour quitter",
            )

    def filter_events(self):
        pass

    def update_event(self, event):
        if not self.permissions.update_event(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.event_opt_menu(event)

        if self._logged_user.departement == models.Departements.GESTION:
            event_data = self.view.prompt_update_event_support(event)
            event_data["contact_support"] = self.repository.get_user(
                event_data["support_email"]
                )

        if self._logged_user.departement == models.Departements.SUPPORT:
            event_data = self.view.prompt_update_event(event)

        response = self.repository.commit()
        if not response:
            self.view.prompt_error_message("erreur lors de la mise à jour")
        self.event_opt_menu(event)

    def delete_event(self, event):
        if not self.permissions.delete_event(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.event_opt_menu(event)

        response = self.repository.delete_event(event)
        if not response:
            self.view.prompt_error_message("erreur lors de la suppression")
        self.view.print("L'évenement à bien été supprimé")
        self.event_menu()

    def quit(self):
        # self.view.exit_message()
        exit()


if __name__ == "__main__":
    pass
