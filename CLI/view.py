
class Views:
    def __init__(self, handler):
        self._handler = handler

    def prompt_welcome_page(self):
        return self._handler.display_welcome_page()

    def prompt_login(self):
        return self._handler.display_login()

    def prompt_display_user_info(self, user_data):
        return self._handler.display_user_info(user_data)
