from backend.models import Departements

COMMERCIAL = Departements.COMMERCIAL
GESTION = Departements.GESTION
SUPPORT = Departements.SUPPORT
ADMIN = Departements.ADMIN


class Permissions:
    def create_user(self, user):
        if user.departement in [ADMIN, GESTION]:
            return True
        return False

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
            return True
        if user == target_user:
            return True
        return False

    def delete_user(self, user):
        if user.departement in [ADMIN, GESTION]:
            return True
        return False

    def create_client(self, user):
        if user.departement in [ADMIN, COMMERCIAL]:
            return True
        return False

    def read_client(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True
        return False

    def update_client(self, user):
        if user.departement in [ADMIN]:
            return True
        return False

    def delete_client(self, user):
        if user.departement in [ADMIN]:
            return True
        return False

    def update_own_clients(self, user, client):
        if user.departement in [COMMERCIAL] and client.commercial_contact == user:
            return True
        return False

    def create_contract(self, user):
        if user.departement in [ADMIN, GESTION]:
            return True
        return False

    def read_contract(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True
        return False

    def update_contract(self, user, contract):
        if user.departement in [ADMIN, GESTION]:
            return True
        if user.departement in [COMMERCIAL] and contract.commercial == user:
            return True
        return False

    def delete_contract(self, user):
        if user.departement in [ADMIN]:
            return True
        return False

    def filter_contract(self, user):
        if user.departement in [ADMIN, COMMERCIAL]:
            return True
        return False

    def create_event(self, user):
        if user.departement in [ADMIN, COMMERCIAL]:
            return True
        return False

    def read_event(self, user):
        if user.departement in [ADMIN, GESTION, SUPPORT, COMMERCIAL]:
            return True
        return False

    def update_event(self, user):
        if user.departement in [ADMIN]:
            return True
        return False

    def delete_event(self, user):
        if user.departement in [ADMIN]:
            return True
        return False

    def add_support_to_event(self, user):
        if user.departement in [ADMIN]:
            return True
        if user.departement in [GESTION]:
            return True
        return False

    def create_event_for_own_client(self, user, contract):
        # if contract is signed
        if user.departement in [ADMIN]:
            return True
        elif user.departement in [COMMERCIAL] and user.contract == contract:
            return True
        return False

    def filter_event(self, user):
        if user.departement in [ADMIN, SUPPORT, GESTION]:
            return True
        return False

    def update_in_charge_event(self, user):
        if user.departement in [ADMIN, SUPPORT, GESTION]:
            return True
        return False
