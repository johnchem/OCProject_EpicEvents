from backend.models import Departements

COMMERCIAL = Departements.COMMERCIAL
GESTION = Departements.GESTION
SUPPORT = Departements.SUPPORT
ADMIN = Departements.ADMIN


class Permissions:
    def create_user(self, user):
        if user.departement in [ADMIN, GESTION]:
            return True, None
        err_msg = "besoin d'un accés admin ou gestion pour cette opération"
        return False, err_msg

    def list_user(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True
        return False

    def read_user(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True
        return False

    def update_user(self, user, target_user):
        if user.departement in [ADMIN, GESTION]:
            return True, None
        elif user == target_user:
            return True, None
        err_msg = "besoin d'un accés admin pour cette opération"
        return False, err_msg

    def delete_user(self, user, target_user):
        if user.departement in [ADMIN, GESTION]:
            return True, None
        err_msg = "besoin d'un accés admin ou faire partis \n de l'équipe gestion pour cette opération"
        return False, err_msg

    def create_client(self, user):
        if user.departement in [ADMIN, COMMERCIAL]:
            return True, None
        err_msg = "besoin d'un accés admin ou faire partis \n de l'équipe gestion pour cette opération"
        return False, err_msg

    def read_client(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True, None
        err_msg = "accés non authorisé"
        return False, err_msg

    def update_client(self, user, client):
        if user.departement in [ADMIN]:
            return True, None
        elif user.departement is COMMERCIAL and client.commercial_contact == user:
            return True, None
        err_msg = "besoin d'un accés admin ou être le commercial en charge pour cette opération"
        return False, err_msg

    def delete_client(self, user, client):
        if user.departement in [ADMIN]:
            return True, None
        elif user.departement is COMMERCIAL and client.commercial_contact == user:
            return True, None
        err_msg = "accés non authorisé"
        return False, err_msg

    def create_contract(self, user, client=None):
        if client is not None and user.departement in [COMMERCIAL] and client in user.client_portfolio:
            return True, None
        elif user.departement in [ADMIN, GESTION, COMMERCIAL]:
            return True, None
        err_msg = "besoin d'un accés admin, gestion ou être le commercial en charge du client pour cette opération"
        return False, err_msg

    def read_contract(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True, None
        return False, None

    def update_contract(self, user, contract):
        if user.departement in [ADMIN, GESTION]:
            return True, None
        if user.departement in [COMMERCIAL] and contract.commercial == user:
            return True, None
        return False, None

    def delete_contract(self, user, contract):
        if user.departement in [ADMIN, GESTION]:
            return True, None
        if user.departement in [COMMERCIAL] and contract.commercial == user:
            return True, None
        return False, None

    def filter_contract(self, user):
        if user.departement in [ADMIN, COMMERCIAL]:
            return True, None
        err_msg = ""
        return False, err_msg

    def create_event(self, user, client):
        if user.departement is ADMIN:
            return True, None
        elif user.departement is COMMERCIAL and client in user.client_portfolio:
            return True, None
        err_msg = "besoin d'un accés admin ou être le commercial en charge pour cette opération"
        return False, err_msg

    def read_event(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True, None
        err_msg = ""
        return False, err_msg

    def update_event(self, user, event):
        if user.departement in [ADMIN]:
            return True, None

        if event.contact_support == None:
            if user.departement is GESTION:
                return True, None
            err_msg = "Un membre Support doit être défini avant de réaliser cette opération"
            return False, err_msg
        else:
            if user.departement is SUPPORT and event.contact_support == user:
                return True, None
            err_msg = "accés limité au membre Support en charge"
            return False, err_msg

    def delete_event(self, user, event):
        if user.departement in [ADMIN]:
            return True, None
        elif event.support == None:
            err_msg = "Un membre Support doit être défini avant de réaliser cette opération"
            return False, err_msg
        elif user.departement is SUPPORT and event.contact_support == user:
            return True, None
        err_msg = "accés limité au membre Support en charge"
        return False, err_msg

    # def add_support_to_event(self, user):
    #     if user.departement in [ADMIN]:
    #         return True, None
    #     if user.departement is GESTION:
    #         return True, None
    #     err_msg = "opération limité à un membre de l'équipe Gestion"
    #     return False, err_msg

    # def create_event_for_own_client(self, user, contract):
    #     # if contract is signed
    #     if user.departement in [ADMIN]:
    #         return True
    #     elif user.departement in [COMMERCIAL] and user.contract == contract:
    #         return True
    #     return False

    def filter_event(self, user):
        if user.departement in [ADMIN, SUPPORT, GESTION]:
            return True
        return False

    def update_in_charge_event(self, user):
        if user.departement in [ADMIN, SUPPORT, GESTION]:
            return True
        return False
