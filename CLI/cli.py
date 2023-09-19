import os
from typing import Optional
from backend.models import Departements

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

    def input(self, msg_obj=None, **kwargs) -> str:
        return self._console.input(msg_obj, **kwargs)

    def print_list(self, msg_list=None) -> None:
        for msg in msg_list:
            self.print(msg)

    def clear(self):
        self._console.clear()


class cli_handler:
    def __init__(self):
        self._display = Display()

    def display_menu(self, menu_item):
        self._display.clear()
        for pos, item in enumerate(menu_item, start=1):
            self._display.print(f"[red][{pos}] : [/red][green]{item}[/green]")
        choice = int(self._display.input("Selection : "))
        return choice

    def display_error_msg(self, msg):
        self._display.error(msg)

    def display_login(self):
        self._display.clear()
        login_prompt = Panel(
            """
                Please entrer your password
            """,
            box=box.ROUNDED,
        )
        self._display.log_styled(login_prompt)
        client_email = self._display.input("Email : ")
        client_password = self._display.input("Password : ", password=True)
        return (client_email, client_password)

    def display_welcome_page(self):
        self._display.clear()
        welcome_prompt = Panel(
            """
                Welcome to Epic Event
            """,
            box=box.ROUNDED,
        )
        self._display.log_styled(welcome_prompt)
        os.system("pause")

    def display_user_info(self, user_data):
        self._display.clear()
        self._display.print(f"[green]Nom : [/green]{user_data.name}")
        self._display.print(f"[green]Prenom : [/green]{user_data.forname}")
        self._display.print(f"[green]@mail : [/green]{user_data.email}")
        self._display.print(f"[green]departement : [/green]{str(user_data.departement.value)}")
        os.system("pause")

    def display_create_user_form(self):
        self._display.clear()
        name = self._display.input("[bolt green]Nom : [/bolt green]")
        forname = self._display.input("[bolt green]Prenom : [/bolt green]")
        email = self._display.input("[bolt green]email : [/bolt green]")
        self._display.print("[bolt green]Departement : [/bolt green]")
        for pos, item in enumerate(Departements, start=1):
            self._display.print(f"[green][{pos}] : [/green]{item.value}")
        dpt_choices = self._display.input()
        departement = [x for x in Departements][dpt_choices-1]
        password = self._display.input(
            "[bolt green]Mot de passe : [/bolt green]",
            password=True
        )
        return {
            "name": name,
            "forname": forname,
            "email": email,
            "departement": departement,
            "password": password,
            }

