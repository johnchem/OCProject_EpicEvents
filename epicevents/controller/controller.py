import functools
import inspect
from sentry_sdk import capture_exception, capture_message

from epicevents.backend.repository import SqlAlchemyRepository
from epicevents.controller.permissions import Permissions
from epicevents.CLI.view import Views
import epicevents.backend.models as models
import epicevents.controller.menu as menu
import epicevents.authentification as auth


def check_user_auth(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        try:
            # get the current token if any
            if self.id_token:
                token = self.id_token
            else:
                token = auth.read_token_from_file()

            if token:
                # check the validity of the token
                auth_user_email, error = auth.verify_jwt_token(token)

                if error == "expired token":
                    # delete old token and refresh it
                    auth.remove_token_file()

                    token = auth.create_id_token(self._logged_user)
                    auth.save_token_to_file(token)
                    self.id_token = token

                elif error == "invalid token":
                    # remove the invalid token and ask for a new authentification
                    token = None
                    self._logged_user = None
                    self.user_login()
            else:
                # no token found : ask for identification
                self.user_login()

            func(self, *args, **kwargs)
        except Exception as err:
            capture_exception(err)
            self.user_login()

    return inner


def visitor_allowed(function):
    function.request_login = False
    return function


def should_be_auth(function):
    try:
        return bool(function.request_login)
    except AttributeError:
        return True


def decorate_all_with(decorator, predicate=None):
    if predicate is None:
        predicate = lambda _: True

    def decorate_all(cls):
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if predicate(method):
                setattr(cls, name, decorator(method))
        return cls

    return decorate_all


@decorate_all_with(check_user_auth, should_be_auth)
class Controller(menu.Menu):
    """Controlleur principal"""

    @visitor_allowed
    def __init__(
        self,
        repository: SqlAlchemyRepository,
        view: Views,
        permissions: Permissions,
    ):
        menu.Menu.__init__(self, view, repository)
        self.permissions = permissions
        self._logged_user = None
        self.id_token = None

    @visitor_allowed
    def welcome_page(self):
        self.view.prompt_welcome_page()

    @visitor_allowed
    def start(self):
        self.welcome_page()
        if not self._logged_user:
            self.user_login()
        self.view.prompt_user_info(self._logged_user)
        self.main_menu()

    @visitor_allowed
    def user_login(self):
        email, password = self.view.prompt_login()

        user = self.repository.get_user(email)
        if not user:
            capture_message(f"wrong user id :{email}", "error")
            self.view.prompt_error_message(f"L'utilisateur {email} n'existe pas")
            self.user_login()

        access_granted = auth.authenticate_user(user, password)

        if access_granted:
            self.id_token = auth.create_id_token(user)
            self._logged_user = user
            auth.save_token_to_file(self.id_token)
        else:
            capture_message(f"wrong password for :{email}", "error")
            self.view.prompt_error_message("Mot de passe incorrect")
            self.user_login()

    # *************** User functions ***************
    def create_user(self, *args, **kwargs):
        access, msg = self.permissions.create_user(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.user_menu()
        data = self.view.prompt_create_user_form()
        user = models.User(**data)

        response, msg = self.repository.add(user)
        if response:
            self.view.prompt_user_info(user)
            capture_message(
                f"{self._logged_user.email} - {self._logged_user.departement.value} - Creation user : {user.email}",
                "info",
            )
            self.user_menu()
        else:
            self.view.prompt_error_message(msg)
            self.user_menu

    def list_user(self, *args, **kwargs):
        users = self.repository.list_user()
        choices = self.view.prompt_list_users(users)
        if choices == "q":
            self.user_menu()
        try:
            choices = int(choices)
            if choices > len(users):
                self.list_user()
            user_picked = users[choices - 1]
            self.view.prompt_user_info(user_picked)
            self.user_opt_menu(user_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                (f"Veuillez choisir une valeur entre 1 et {len(users)}" + "\n ou q pour quitter")
            )
            self.user_opt_menu(user_picked)

    def update_user(self, user):
        access, msg = self.permissions.update_user(self._logged_user, user)
        if not access:
            self.view.prompt_error_message(msg)
            self.user_opt_menu(user)

        # update_user_gen = self.repository.update_user(user.id)
        user_data = self.repository.get_user(user.email)
        user_data = self.view.prompt_display_update_user(user_data)

        # response = update_user_gen.send(user_data)
        response, err = self.repository.commit()
        if not response:
            self.view.prompt_error_message(f"erreur lors de la mise à jour\n{err}")
            self.user_opt_menu(user)

        capture_message(
            f"{self._logged_user.email} - {self._logged_user.departement.value} - update user :{user.email}", "info"
        )
        self.user_menu()

    def delete_user(self, user_data, *args, **kwargs):
        access, msg = self.permissions.delete_user(self._logged_user, user_data)
        if not access:
            self.view.prompt_error_message(msg)
            self.user_opt_menu(user_data)

        response, msg = self.repository.delete_user(user_data)
        if not response:
            self.view.prompt_error_message(msg)
            self.user_opt_menu(user_data)
        capture_message(
            f"{self._logged_user.email} - {self._logged_user.departement.value} - user deletion : {user_data.email}",
            "info",
        )
        self.view.prompt_message("L'utilisateur à bien été supprimé")
        self.user_menu()

    # ************** Client functions **************
    def create_client(self):
        access, msg = self.permissions.create_client(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.user_menu()
        else:
            default_commercial = self._logged_user
            data = self.view.prompt_create_client()
            while True:
                commercial_mail = self.view.prompt_ask_commercial(default_commercial.email)
                if commercial_mail != default_commercial.email:
                    commercial = self.repository.get_user(commercial_mail)
                else:
                    commercial = default_commercial

                if commercial is None:
                    self.view.prompt_error_message("L'utilisateur n'existe pas")
                    continue
                if commercial.departement == models.Departements.COMMERCIAL:
                    break
                self.view.prompt_error_message("Ce membre ne fait pas partis de l'équipe commercial")

            data["commercial_contact"] = commercial
            client = models.Client(**data)
            response, msg = self.repository.add(client)

        if not response:
            self.view.prompt_error_message(msg)
            self.user_menu()
        capture_message(
            f"{self._logged_user.email} - {self._logged_user.departement.value} - client creation {client.full_name}",
            "info",
        )
        self.view.prompt_client_info(client)
        self.main_menu()

    def list_client(self):
        access, msg = self.permissions.read_client(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.user_menu()

        client = self.repository.list_client()
        choices = self.view.prompt_list_client(client)
        if choices == "q":
            self.client_menu()
        try:
            choices = int(choices)
            if choices > len(client):
                self.list_client()
            client_picked = client[choices - 1]
            self.view.prompt_client_info(client_picked)
            self.client_opt_menu(client_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(client)}",
                "ou q pour quitter",
            )
            self.client_opt_menu(client_picked)

    def update_client(self, client):
        access, msg = self.permissions.update_client(self._logged_user, client)
        if not access:
            self.view.prompt_error_message(msg)
            self.client_opt_menu(client)

        updated_client = self.view.prompt_update_client(client)
        while True:
            commercial_mail = self.view.prompt_ask_commercial(updated_client.commercial_contact.email)
            if commercial_mail == client.commercial_contact.email:
                break
            commercial = self.repository.get_user(commercial_mail)
            if commercial is None:
                self.view.prompt_error_message("L'utilisateur n'existe pas")
                continue
            if commercial.departement == models.Departements.COMMERCIAL:
                updated_client.commercial_contact = commercial
                break
            self.view.prompt_error_message("Ce membre ne fait pas partis de l'équipe commercial")

        # response = update_user_gen.send(user_data)
        response, err = self.repository.commit()
        if not response:
            self.view.prompt_error_message(f"erreur lors de la mise à jour du client\n{err}")
            self.client_opt_menu(client)

        self.view.prompt_client_info(updated_client)
        capture_message(
            (
                f"{self._logged_user.email} -",
                f" {self._logged_user.departement.value} -",
                f" update client {updated_client.full_name}",
            ),
            "info",
        )
        self.client_menu()

    def delete_client(self, client):
        access, msg = self.permissions.delete_client(self._logged_user, client)
        if not access:
            self.view.prompt_error_message(msg)
            self.client_opt_menu(client)

        response, msg = self.repository.delete_user(client)
        if not response:
            self.view.prompt_error_message(msg)
            self.client_opt_menu(client)
        capture_message(
            f"{self._logged_user.email} - {self._logged_user.departement.value} - client deletion :{client.full_name}",
            "info",
        )
        self.view.print("Le client à bien été supprimé")
        self.client_menu()

    # ************* Contracts functions *************
    def create_contract(self, client=None):
        access, msg = self.permissions.create_contract(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            if client:
                self.client_opt_menu(client)
            else:
                self.contract_menu()

        data = self.view.prompt_ask_client(client=client)
        updated_client = self.repository.get_client(data["client"])
        if updated_client is None:
            self.view.prompt_error_message("Ce client n'est pas enregistré")
            self.contract_menu()

        access, msg = self.permissions.create_contract(self._logged_user, updated_client)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_menu()

        data = self.view.prompt_create_contract()
        data["client"] = updated_client

        contract = models.Contract(**data)
        response, msg = self.repository.add(contract)

        if not response:
            self.view.prompt_error_message(msg)
            if client:
                self.client_opt_menu(client)
            else:
                self.contract_menu()

        capture_message(
            (
                f"{self._logged_user.email} -",
                f" {self._logged_user.departement.value} -",
                f" contract creation for :{contract.client.full_name}",
            ),
            "info",
        )
        self.view.prompt_contract_info(contract)
        self.contract_menu()

    def list_contract(self):
        access, msg = self.permissions.read_contract(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_menu()
        contracts = self.repository.list_contract()
        choices = self.view.prompt_list_contract(contracts)
        if choices == "q":
            self.contract_menu()
        try:
            choices = int(choices)
            if choices > len(contracts):
                self.list_contract()
            contract_picked = contracts[choices - 1]
            self.view.prompt_contract_info(contract_picked)
            self.contract_opt_menu(contract_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(contracts)} ou q pour quitter",
            )
            self.contract_opt_menu(contract_picked)

    def filter_contract_signed(self, *args, **kwargs):
        access, msg = self.permissions.filter_contract(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_menu()
        contracts = self.repository.filter_by_signed_contract()
        choices = self.view.prompt_list_contract(contracts)
        if choices == "q":
            self.contract_menu()
        try:
            choices = int(choices)
            if choices > len(contracts):
                self.filter_contract_signed(*args, **kwargs)
            contract_picked = contracts[choices - 1]
            self.view.prompt_contract_info(contract_picked)
            self.contract_opt_menu(contract_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(contracts)} ou q pour quitter",
            )
            self.contract_opt_menu(contract_picked)

    def filter_contract_not_signed(self, *args, **kwargs):
        access, msg = self.permissions.filter_contract(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_menu()
        contracts = self.repository.filter_by_not_signed_contract()
        choices = self.view.prompt_list_contract(contracts)
        if choices == "q":
            self.contract_menu()
        try:
            choices = int(choices)
            if choices > len(contracts):
                self.filter_contract_not_signed(*args, **kwargs)
            contract_picked = contracts[choices - 1]
            self.view.prompt_contract_info(contract_picked)
            self.contract_opt_menu(contract_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(contracts)} ou q pour quitter",
            )
            self.contract_opt_menu(contract_picked)

    def filter_contract_by_commercial(self, commercial, *args, **kwargs):
        access, msg = self.permissions.filter_contract(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_menu()
        contracts = self.repository.filter_contract_by_commercial(commercial)
        choices = self.view.prompt_list_contract(contracts)
        if choices == "q":
            self.contract_menu()
        try:
            choices = int(choices)
            if choices > len(contracts):
                self.filter_contract_by_commercial(*args, **kwargs)
            contract_picked = contracts[choices - 1]
            self.view.prompt_contract_info(contract_picked)
            self.contract_opt_menu(contract_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(contracts)} ou q pour quitter",
            )
            self.contract_opt_menu(contract_picked)

    def filter_contract_not_fully_paid(self, *args, **kwargs):
        access, msg = self.permissions.filter_contract(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_menu()
        contracts = self.repository.filter_contract_not_fully_paid()
        choices = self.view.prompt_list_contract(contracts)
        if choices == "q":
            self.contract_menu()
        try:
            choices = int(choices)
            if choices > len(contracts):
                self.filter_contract_not_fully_signed()
            contract_picked = contracts[choices - 1]
            self.view.prompt_contract_info(contract_picked)
            self.contract_opt_menu(contract_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(contracts)} ou q pour quitter",
            )
            self.contract_opt_menu(contract_picked)

    def update_contract(self, contract):
        access, msg = self.permissions.update_contract(self._logged_user, contract)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_opt_menu(contract)

        contract = self.view.prompt_update_contract(
            contract,
            client_fullname=contract.client.full_name,
            commercial_email=contract.commercial.email,
        )
        response, err = self.repository.commit()

        if not response:
            self.view.prompt_error_message(f"erreur lors de la mise à jour du contrat\n{err}")
            self.contract_opt_menu(contract)
        capture_message(
            (
                f"{self._logged_user.email} -",
                f" {self._logged_user.departement.value} -",
                f" update contract {contract.client.full_name}",
            ),
            "info",
        )
        self.contract_menu()

    def delete_contract(self, contract):
        access, msg = self.permissions.delete_contract(self._logged_user, contract)
        if not access:
            self.view.prompt_error_message("accés non authorisé")
            self.contract_opt_menu(contract)

        response, msg = self.repository.delete_contract(contract)
        if not response:
            self.view.prompt_error_message(msg)
            self.contract_opt_menu(contract)

        capture_message(
            (
                f"{self._logged_user.email} -",
                f" {self._logged_user.departement.value} -",
                f" contract deletion :{contract.full_name}",
            ),
            "info",
        )
        self.view.print("Le contrat à bien été supprimé")
        self.contract_menu()

    # *************** Events functions ***************
    def create_event(self, contract):
        client = contract.client
        access, msg = self.permissions.create_event(self._logged_user, client)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_opt_menu(contract)

        if contract.contract_status == models.ContractStatus.SIGNED:
            event_data = self.view.prompt_create_event(contract=contract)
            event_data["client"] = contract.client
            event_data["contract"] = contract
            event = models.Evenement(**event_data)
            response, msg = self.repository.add(event)

            if not response:
                self.view.prompt_error_message(msg)
                self.contract_opt_menu(contract)

            capture_message(
                f"{self._logged_user.email} - {self._logged_user.departement.value} - event creation {event.name}",
                "info",
            )
            self.view.prompt_event_info(event)
            self.contract_opt_menu(contract)
        else:
            self.view.prompt_error_message("Le contrat doit être signé pour crée un évenement")
            self.contract_opt_menu(contract)

    def list_events(self):
        access, msg = self.permissions.read_event(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.event_menu()

        event = self.repository.list_event()
        choices = self.view.prompt_list_event(event)
        if choices == "q":
            self.event_menu()
        try:
            choices = int(choices)
            if choices > len(event):
                self.list_events()
            event_picked = event[choices - 1]
            self.view.prompt_event_info(event_picked)
            self.event_opt_menu(event_picked)

        except ValueError as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(event)}",
                "ou q pour quitter",
            )
        except Exception as err:
            self.view.print(err)
            capture_exception(err)
        else:
            self.event_opt_menu(event_picked)

    def update_event(self, event):
        access, msg = self.permissions.update_event(self._logged_user, event)
        if not access:
            self.view.prompt_error_message(msg)
            self.event_opt_menu(event)

        if self._logged_user.departement == models.Departements.GESTION:
            support_email = self.view.prompt_update_event_support(event)
            support = self.repository.get_user(support_email)

            if support is None:
                self.view.prompt_error_message("L'utilisateur n'existe pas")
                self.event_opt_menu(event)
            elif support.departement is not models.Departements.SUPPORT:
                self.view.prompt_error_message("L'utilisateur n'est pas membre de l'équipe Support")
                self.event_opt_menu(event)
            event.contact_support = support

        if self._logged_user.departement == models.Departements.SUPPORT:
            event = self.view.prompt_update_event(event)

        response, err = self.repository.commit()
        if not response:
            self.view.prompt_error_message(f"erreur lors de la mise à jour de l'évenement\n{err}")
            self.event_opt_menu(event)
        capture_message(
            f"{self._logged_user.email} - {self._logged_user.departement.value} - update event {event.name}", "info"
        )
        self.event_opt_menu(event)

    def delete_event(self, event):
        access, msg = self.permissions.delete_event(self._logged_user, event)
        if not access:
            self.view.prompt_error_message(msg)
            self.event_opt_menu(event)

        response, msg = self.repository.delete_event(event)
        if not response:
            self.view.prompt_error_message(msg)
            self.event_opt_menu(event)

        capture_message(
            f"{self._logged_user.email} - {self._logged_user.departement.value} - event deletion {event.name}", "info"
        )
        self.view.print("L'évenement à bien été supprimé")
        self.event_menu()

    def filter_events_without_support(self):
        access, msg = self.permissions.filter_event(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.contract_menu()
        events = self.repository.filter_events_without_support()
        choices = self.view.prompt_list_event(events)
        if choices == "q":
            self.event_menu()
        try:
            choices = int(choices)
            if choices > len(events):
                self.filter_events_without_support()
            event_picked = events[choices - 1]
            self.view.prompt_event_info(event_picked)
            self.event_opt_menu(event_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(events)} ou q pour quitter",
            )
            self.contract_opt_menu(event_picked)

    def filter_my_event(self):
        access, msg = self.permissions.filter_event(self._logged_user)
        if not access:
            self.view.prompt_error_message(msg)
            self.event_menu()
        events = self.repository.filter_events_by_support(self._logged_user)
        choices = self.view.prompt_list_event(events)
        if choices == "q":
            self.event_menu()
        try:
            choices = int(choices)
            if choices > len(events):
                self.filter_my_event()
            event_picked = events[choices - 1]
            self.view.prompt_event_info(event_picked)
            self.event_opt_menu(event_picked)

        except Exception as err:
            self.view.print(err)
            capture_exception(err)
            self.view.prompt_error_message(
                f"Veuillez choisir une valeur entre 1 et {len(events)} ou q pour quitter",
            )
            self.event_opt_menu(event_picked)

    # *************** Closure functions ***************
    def logoff(self):
        auth.remove_token_file()
        self.user_login()
        if self._logged_user:
            self.main_menu()

    def quit(self):
        # self.view.exit_message()
        auth.remove_token_file()
        exit()


if __name__ == "__main__":
    pass
