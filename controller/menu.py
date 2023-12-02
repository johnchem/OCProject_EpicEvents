from abc import ABC, abstractmethod


class Menu(ABC):
    def __init__(self, view, repository):
        self.view = view
        self.repository = repository

    def main_menu(self, *args, **kwargs):
        MENU_ITEM_DICT = {
            "Utilisateurs": self.user_menu,
            "Client": self.client_menu,
            "Contrat": self.contract_menu,
            "Evenements": self.event_menu,
            "Déconnection": self.logoff,
            "Quitter": self.quit,
        }
        # get the list of item for the main menu
        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_main_menu(menu_item_list) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user()

    def user_menu(self, *args, **kwargs):
        MENU_ITEM_DICT = {
            "Affichage des utilisateurs": self.list_user,
            "Ajouter un utilisateur": self.create_user,
            "Retour": self.main_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_user_menu(menu_item_list) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user()

    def user_opt_menu(self, user_data, *args, **kwargs):
        MENU_ITEM_DICT = {
            "Modifier": self.update_user,
            "Supprimer": self.delete_user,
            "Retour": self.user_menu,
        }
        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]

        user_answer = self.view.prompt_user_opt_menu(menu_item_list, user_data) - 1

        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user(user_data)

    def client_menu(self):
        MENU_ITEM_DICT = {
            "Liste des clients": self.list_client,
            "Nouveau client": self.create_client,
            "Retour": self.main_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_client_menu(menu_item_list) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user()

    def client_opt_menu(self, client_data, *args, **kwargs):
        MENU_ITEM_DICT = {
            "Modifier": self.update_client,
            "Créer nouveau contrat": self.create_contract,
            "Créer un nouveau evenénement": self.create_event,
            "Supprimer": self.delete_client,
            "Retour": self.main_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_client_opt_menu(menu_item_list, client_data) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user(client=client_data)

    def contract_menu(self):
        MENU_ITEM_DICT = {
            "Liste des contrats": self.list_contract,
            "Filter les contrats": self.filter_contract_menu,
            "Créer un contrat": self.create_contract,
            "Retour": self.main_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_contract_menu(menu_item_list) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user()

    def contract_opt_menu(self, contract_data):
        MENU_ITEM_DICT = {
            "Modifier": self.update_contract,
            "Créer evenement": self.create_event,
            "Supprimer": self.delete_contract,
            "Retour": self.main_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_contract_opt_menu(menu_item_list, contract_data) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user(contract=contract_data)

    def filter_contract_menu(self):
        if not self.permissions.filter_contract(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.contract_menu()

        MENU_ITEM_DICT = {
            "Contrat en cours": self.filter_contract_not_signed,
            "Contrat en signés": self.filter_contract_signed,
            "Mes contrats": self.filter_contract_by_commercial,
            "Filtrer par commerciaux": self.filter_by_commercial_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_filter_contract_menu(menu_item_list) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user(commercial=self._logged_user)

    def filter_by_commercial_menu(self, *args, **kwargs):
        commercials = self.repository.list_commercial_with_contract()

        menu_item_list = [x.email for x in commercials]
        user_answer = int(self.view.prompt_filter_contract_menu(menu_item_list) - 1)
        # convert the answer to the function
        commercial = commercials[user_answer]
        # Call the function
        self.filter_contract_by_commercial(commercial=commercial)

    def event_menu(self):
        MENU_ITEM_DICT = {
            "Liste des evenements": self.list_events,
            "Filter les evenements": self.filter_event_menu,
            "Retour": self.main_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_event_menu(menu_item_list) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user()

    def event_opt_menu(self, event):
        MENU_ITEM_DICT = {
            "Modifier": self.update_event,
            "Supprimer": self.delete_event,
            "Retour": self.main_menu,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_event_opt_menu(menu_item_list, event) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user()

    def filter_event_menu(self):
        if not self.permissions.filter_event(self._logged_user):
            self.view.prompt_error_message("accés non authorisé")
            self.event_menu()

        MENU_ITEM_DICT = {
            "Evenement sans support": self.filter_events_without_support,
            "Mes evenements": self.filter_my_event,
        }

        menu_item_list = [x for x in MENU_ITEM_DICT.keys()]
        user_answer = self.view.prompt_filter_event_menu(menu_item_list) - 1
        # convert the answer to the function
        function_called_by_user = MENU_ITEM_DICT[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user(commercial=self._logged_user)

    @abstractmethod
    def create_user(self):
        pass

    @abstractmethod
    def list_user(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def delete_user(self):
        pass

    @abstractmethod
    def create_client(self):
        pass

    @abstractmethod
    def list_client(self):
        pass

    @abstractmethod
    def update_client(self):
        pass

    @abstractmethod
    def delete_client(self):
        pass

    @abstractmethod
    def create_contract(self):
        pass

    @abstractmethod
    def list_contract(self):
        pass

    @abstractmethod
    def update_contract(self):
        pass

    @abstractmethod
    def delete_contract(self):
        pass

    @abstractmethod
    def create_event(self):
        pass

    @abstractmethod
    def list_events(self):
        pass

    @abstractmethod
    def update_event(self):
        pass

    @abstractmethod
    def delete_event(self):
        pass

    @abstractmethod
    def logoff(self):
        pass

    @abstractmethod
    def quit(self):
        pass
