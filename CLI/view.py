
class Views:
    def __init__(self, handler):
        self._handler = handler

    def print(self, msg_obj):
        return self._handler.print(msg_obj)

    def prompt_welcome_page(self):
        return self._handler.display_welcome_page()

    def prompt_login(self):
        return self._handler.display_login()
    
    def prompt_display_menu(self, menu_item):
        return self._handler.display_menu(menu_item)

    def prompt_error_message(self, msg):
        return self._handler.display_error_msg(msg)
    
    def prompt_main_menu(self, menu_item):
        self._handler.clear()
        self._handler.print("[i]Menu principal[/i]")
        return self._handler.display_menu(menu_item)

    # -------- User views --------------
    def prompt_display_user_info(self, user_data):
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

    def prompt_client_opt_menu(self, menu_item):
        self._handler.clear()
        return self._handler.display_menu(menu_item)

    def prompt_client_info(self, client_data):
        return self._handler.display_client_info(client_data)

    def prompt_create_client(self, default_commercial):
        self._handler.clear()
        return self._handler.display_create_client_form(default_commercial)

    def prompt_update_client(self, client_data):
        self._handler.clear()
        return self._handler.display_update_client_form(client_data)

    def prompt_list_client(self, client_list):
        self._handler.clear()
        return self._handler.display_list_client(client_list)
