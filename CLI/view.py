from authentification import encode_decode_jwt, encode, decode


class Views:
    def __init__(self, handler):
        self._handler = handler

    def print(self, token):
        data = decode(token)
        msg_obj = data.get("msg_obj")
        return self._handler.print(msg_obj)
    
    def prompt_welcome_page(self):
        return self._handler.display_welcome_page()

    def prompt_login(self):
        email, password = self._handler.display_login()
        response = {
            "email": email,
            "password":password
            }
        token = encode(response)
        return token

    def prompt_display_menu(self, menu_item):
        return self._handler.display_menu(menu_item)

    def prompt_error_message(self, msg):
        return self._handler.display_error_msg(msg)

    def prompt_main_menu(self, menu_item):
        self._handler.clear()
        self._handler.print("[i]Menu principal[/i]")
        return self._handler.display_menu(menu_item)

    # -------- User views --------------
    def prompt_user_info(self, user_data):
        return self._handler.display_user_info(user_data)

    def prompt_user_header(self, user_data):
        return self._handler.display_user_header(user_data)

    def prompt_create_user_form(self):
        return self._handler.display_create_user_form()

    def prompt_list_users(self, users_list):
        self._handler.clear()
        return self._handler.display_list_user(users_list)

    def prompt_user_opt_menu(self, menu_item, user_data):
        self._handler.clear()
        self._handler.display_user_header(user_data)
        return self._handler.display_menu(menu_item)

    def prompt_user_menu(self, menu_item):
        self._handler.clear()
        self._handler.print("[i]Menu utilisateur[/i]")
        return self._handler.display_menu(menu_item)

    def prompt_display_update_user(self, data):
        self._handler.clear()
        return self._handler.display_update_user_form(data)

    # -------- Client views --------------
    def prompt_client_menu(self, menu_item):
        self._handler.clear()
        self._handler.print("[i]Menu client[/i]")
        return self._handler.display_menu(menu_item)

    def prompt_client_opt_menu(self, menu_item, client):
        self._handler.clear()
        return self._handler.display_menu(menu_item)

    def prompt_client_info(self, client_data):
        self._handler.clear()
        return self._handler.display_client_info(client_data)

    def prompt_create_client(self):
        self._handler.clear()
        return self._handler.display_create_client_form()

    def prompt_update_client(self, client_data):
        self._handler.clear()
        return self._handler.display_update_client_form(client_data)

    def prompt_list_client(self, client_list):
        self._handler.clear()
        return self._handler.display_list_client(client_list)

    def prompt_ask_commercial(self, default_commercial):
        return self._handler.display_ask_commercial(default_commercial)

    # -------- Contract views --------------
    def prompt_contract_menu(self, menu_item):
        self._handler.clear()
        self._handler.print("[i]Menu contrat[/i]")
        return self._handler.display_menu(menu_item)

    def prompt_contract_opt_menu(self, menu_item, contract):
        self._handler.clear()
        self._handler.display_contract_header(contract)
        return self._handler.display_menu(menu_item)

    def prompt_create_contract(self, client=None):
        self._handler.clear()
        return self._handler.display_create_contract(client)

    def prompt_update_contract(self, contract, client_fullname, commercial_email):
        self._handler.clear()
        return self._handler.display_update_contract_form(contract, client_fullname, commercial_email)

    def prompt_contract_info(self, client):
        self._handler.clear()
        return self._handler.display_contract_info(client)

    def prompt_list_contract(self, contract_list):
        self._handler.clear()
        return self._handler.display_list_contract(contract_list)
    
    def prompt_filter_contract_menu(self, menu_item):
        self._handler.clear()
        self._handler.print("[i]Menu filtrage de contrat[/i]")
        return self._handler.display_menu(menu_item)

    def prompt_contract_filter_by_commercial_menu(self, list_commercial):
        self._handler.clear()
        self._handler.print("[i]Selection commercial[/i]")
        return self._handler.display_menu(list_commercial)

    # -------- Event views --------------
    def prompt_event_menu(self, menu_item):
        self._handler.clear()
        self._handler.print("[i]Menu Evenements")
        return self._handler.display_menu(menu_item)

    def prompt_event_opt_menu(self, menu_item, event):
        self._handler.clear()
        self._handler.display_event_header(event)
        return self._handler.display_menu(menu_item)

    def prompt_create_event(self, contract):
        self._handler.clear()
        return self._handler.display_create_event(contract)

    def prompt_list_event(self, event_list):
        self._handler.clear()
        return self._handler.display_list_event(event_list)

    def prompt_event_info(self, event):
        self._handler.clear()
        self._handler.display_event_info(event)

    def prompt_update_event(self, event):
        self._handler.clear()
        return self._handler.display_event_update(event)

    def prompt_update_event_support(self, event):
        self._handler.clear()
        return self._handler.display_event_define_support(event)
