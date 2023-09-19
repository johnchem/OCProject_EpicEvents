
class Views:
    def __init__(self, handler):
        self._handler = handler

    def prompt_welcome_page(self):
        return self._handler.display_welcome_page()

    def prompt_login(self):
        return self._handler.display_login()

    def prompt_display_user_info(self, user_data):
        return self._handler.display_user_info(user_data)

    def prompt_create_user_form(self):
        return self._handler.display_create_user_form()

    def prompt_display_menu(self, menu_item):
        return self._handler.display_menu(menu_item)

    def prompt_error_message(self, msg):
        return self._handler.display_error_msg(msg)

    def prompt_display_client_info(self, client_data):
        return self._handler.display_client_info(client_data)

    def prompt_display_update_user(self, data):
        return self._handler.display_update_user(data)
