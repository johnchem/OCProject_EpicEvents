
class Permissions:
    def create_user(self, user):
        if user.departement.value in ["Administrator", "Commercial"]:
            return True
        return False

    def list_user(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def read_user(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def update_user(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def delete_user(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def create_client(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def read_client(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def update_client(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def delete_client(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def update_own_clients(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def create_contract(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def read_contract(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def update_contract(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def delete_contract(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def update_own_contract(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def filter_contract(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def create_event(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def read_event(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def update_event(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def delete_event(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def add_support_to_event(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def create_event_for_own_client(self, user):
        # if contrat is signed
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def filter_event(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False

    def update_in_charge_event(self, user):
        if user.departement.value in ["Administrator"]:
            return True
        return False
