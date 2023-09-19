from abc import ABC, abstractmethod


class Menu(ABC):
    def __init__(self, view):
        self.view = view

    def menu_handler(self, menu_dict):
        # get the list of item for the main menu
        menu_item_list = [x for x in menu_dict.keys()]

        user_answer = (
            self.view.prompt_display_menu(menu_item_list)-1
        )

        # convert the answer to the function
        function_called_by_user = menu_dict[menu_item_list[user_answer]]
        # Call the function
        function_called_by_user()

    def main_menu(self):
        MENU_ITEM_DICT = {
            "Utilisateurs": self.user_menu,
            "Client": self.client_menu,
            "Contrat": self.contract_menu,
            "Evenements": self.event_menu,
            "Quitter": self.quit,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def user_menu(self):
        MENU_ITEM_DICT = {
            "Affichage des utilisateurs": self.list_user,
            "Ajouter un utilisateur": self.create_user,
            "Retour": self.main_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def user_opt_menu(self):
        MENU_ITEM_DICT = {
            "Modifier": self.update_user,
            "Supprimer": self.delete_user,
            "Retour": self.user_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def client_menu(self):
        MENU_ITEM_DICT = {
            "Nouveau client": self.create_client,
            "Liste des clients": self.list_client,
            "Retour": self.main_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def client_opt_menu(self):
        MENU_ITEM_DICT = {
            "Modifier": self.update_client,
            "Créer nouveau contrat": self.create_contract,
            "Créer un nouveau evenénement": self.create_event,
            "Supprimer": self.delete_client,
            "Retour": self.main_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def contract_menu(self):
        MENU_ITEM_DICT = {
            "Liste des contrats": self.list_contract,
            "Filter les contrats": self.filter_contract,
            "Retour": self.main_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def contract_opt_menu(self):
        MENU_ITEM_DICT = {
            "Modifier": self.update_contract,
            "Créer evenement": self.create_event,
            "Supprimer": self.delete_contract,
            "Retour": self.main_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def event_menu(self):
        MENU_ITEM_DICT = {
            "Liste des evenements": self.list_events,
            "Filter les evenements": self.filter_events,
            "Retour": self.main_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

    def event_opt_menu(self):
        MENU_ITEM_DICT = {
            "Modifier": self.update_event,
            "Supprimer": self.delete_event,
            "Retour": self.main_menu,
        }

        self.menu_handler(MENU_ITEM_DICT)

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
    def filter_contract(self):
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
    def filter_events(self):
        pass

    @abstractmethod
    def update_event(self):
        pass

    @abstractmethod
    def delete_event(self):
        pass

    @abstractmethod
    def quit(self):
        pass
