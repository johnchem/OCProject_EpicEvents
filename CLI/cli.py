import os
import getpass
from typing import Optional

from rich import box
from rich.console import Console
from rich.panel import Panel


class Display:
    def __init__(self):
        self._console = Console()

    def print(self, msg_obj=None) -> None:
        self._console.print(msg_obj)

    def log(self, msg_obj=None) -> None:
        self._console.print(msg_obj, style="bold green")

    def log_styled(self, msg_obj=None, style: Optional[str] = None) -> None:
        self._console.print(msg_obj, style=style)

    def warning(self, msg_obj=None) -> None:
        self._console.print(msg_obj, style="bold yellow")

    def error(self, msg_obj=None) -> None:
        self._console.print(msg_obj, style="bold red")


class cli_handler:
    def __init__(self):
        self._display = Display()

    def display_login(self):
        login_prompt = Panel(
            """
                Please entrer your password
            """,
            box=box.ROUNDED,
        )
        self._display.log_styled(login_prompt)
        client_email = input("Email : ")
        client_password = getpass.getpass(prompt="Password : ")
        return (client_email, client_password)

    def display_welcome_page(self):
        welcome_prompt = Panel(
            """
                Welcome to Epic Event
            """,
            box=box.ROUNDED,
        )
        self._display.log_styled(welcome_prompt)
        os.system("pause")

    def display_user_info(self, user_data):
        self._display.print(f"[green]Nom : [/green]{user_data.name}")
        self._display.print(f"[green]Prenom : [/green]{user_data.forname}")
        self._display.print(f"[green]@mail : [/green]{user_data.email}")
        self._display.print(f"[green]departement : [/green]{str(user_data.departement.value)}")
        os.system("pause")

