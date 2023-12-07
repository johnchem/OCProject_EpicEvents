from datetime import datetime
import os
from typing import Optional
from backend.models import ContractStatus, Departements

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.padding import Padding

from backend.models import DT_STRING


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

    def ask(self, msg_obj=None, default=None, choices=None, int=False, *args, **kwargs):
        if int:
            return IntPrompt.ask(msg_obj, choices=choices, default=default, *args, **kwargs)
        else:
            return Prompt.ask(msg_obj, choices=choices, default=default, *args, **kwargs)

    def clear(self):
        self._console.clear()


class cli_handler:
    def __init__(self):
        self._display = Display()

    def clear(self):
        self._display.clear()

    def print(self, msg_obj):
        self._display.print(msg_obj)

    def display_menu(self, menu_item):
        for pos, item in enumerate(menu_item, start=1):
            self._display.print(f"[red][{pos}] : [/red][green]{item}[/green]")
        choice = ""
        correct_answer = False
        while not correct_answer:
            choice = self._display.input("Selection : ")
            if choice.isnumeric():
                choice = int(choice)
            else:
                choice = self._display.error("Introduire un nombre")
                continue
            if choice == 0 or choice > len(menu_item):
                self._display.error(f"Veuillez choisir une valeur entre 1 et {len(menu_item)}")
                continue
            correct_answer = True

        return choice

    def display_error_msg(self, msg, pause=True):
        self._display.error(msg)
        if pause:
            os.system("pause")

    def display_msg(self, msg, pause=True):
        self._display.print(msg)
        if pause:
            os.system("pause")

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

    def display_user_header(self, user_data):
        grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
        grid.add_column(justify="center")
        grid.add_column(justify="center")

        grid.add_row(f"[green]{user_data.name.upper()}[/green]", f"[green]{user_data.forname}[/green]")
        grid.add_row(f"[green]{user_data.email}[/green]", f"[blue]{str(user_data.departement.value)}[/blue]")
        self._display.print(grid)

    def display_create_user_form(self):
        while True:
            try:
                name = self._display.input("[green]Nom : [/green]")
                forname = self._display.input("[green]Prenom : [/green]")
                email = self._display.input("[green]email : [/green]")
                self._display.print("[green]Departement : [/green]")
                for pos, item in enumerate(Departements, start=1):
                    self._display.print(f"[green][{pos}] : [/green]{item.value}")
                dpt_choices = int(self._display.input())
                departement = [x for x in Departements][dpt_choices - 1]
                password = self._display.input("[green]Mot de passe : [/green]", password=True)
                break
            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la creation : {err}")
        return {
            "name": name,
            "forname": forname,
            "email": email,
            "departement": departement,
            "password": password,
        }

    def display_update_user_form(self, user_data):
        while True:
            try:
                user_data.name = self._display.ask("[green]Nom [/green]", default=user_data.name)
                user_data.forname = self._display.ask("[green]Prenom [/green]", default=user_data.forname)
                user_data.email = self._display.ask("[green]email [/green]", default=user_data.email)
                self._display.print("[green]Departement [/green]")
                for pos, item in enumerate(Departements, start=1):
                    if item == user_data.departement:
                        default_pos = pos
                    self._display.print(f"[green][{pos}] : [/green]{item.value}")
                dpt_choices = self._display.ask(
                    f"[green]Departement [/green][blue]{user_data.departement.value}[/blue]",
                    default=default_pos,
                    int=True,
                )
                user_data.departement = [x for x in Departements][dpt_choices - 1]
                user_data.password = self._display.ask("[green]Mot de passe : [/green]", password=True)
                break
            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la mise à jour : {err}")
        return user_data

    def display_client_info(self, client_data):
        grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
        grid.add_column(justify="center")
        grid.add_column(justify="center")

        grid.add_row(
            f"[purple]{client_data.full_name}[/purple]",
            f"[purple]{client_data.email}[/purple]",
        )
        grid.add_row(
            f"[purple]{client_data.phone}[/purple]",
            "",
        )
        grid.add_row(
            f"[purple]{client_data.company_name}[/purple]",
            "",
        )
        grid.add_row("[green]Date de creation :[/green]", f"[blue]{client_data.creation_date}[/blue]")
        grid.add_row("[green]Derniére mise à jour :[/green]", f"[blue]{client_data.last_update}[/blue]")
        grid.add_row(
            "[green]Responsable client[/green]",
            f"[blue]{client_data.commercial_contact.forname} {client_data.commercial_contact.name.upper()}[/blue]",
        )
        self._display.print(grid)

        self._display.print(Padding("[green u]Contrats actif[/green u]", (1, 0, 0, 0)))
        if client_data.contract:
            # self._display.print(f"{client_data.contract}")
            for contract in client_data.contract:
                self._display.print(f"{contract}")
        else:
            self._display.print("[i] ... pas de contrat[/i]")

        self._display.print(Padding("[green u]Evenement actif[/green u]", (1, 0, 0, 0)))
        if client_data.evenements:
            for event in client_data.evenements:
                self._display.print(repr(event))
        else:
            self._display.print("[i] ... pas d'évenement[/i]")
        os.system("pause")

    def display_list_user(self, user_list):
        table = Table(title="Utilisateurs")
        table.add_column("Id", justify="center", style="red")
        table.add_column("Nom", justify="center", style="green")
        table.add_column("Email", justify="center")
        table.add_column("Departement", justify="center", style="cyan")

        for pos, user in enumerate(user_list, start=1):
            table.add_row(
                f"{pos}",
                f"{user.name.upper()} {user.forname}",
                f"{user.email}",
                f"{user.departement.value}",
            )
        self._display.print(table)
        self._display.print("Selectionner un utilisateur ou q pour revenir")
        return self._display.input()

    def display_list_client(self, client_list):
        table = Table(title="Clients")
        table.add_column("Id", justify="center", style="red")
        table.add_column("Personne de contact", justify="center", style="cyan")
        table.add_column("Mail", justify="center")
        table.add_column("Telephone", justify="center")
        table.add_column("Commercial", justify="center", style="red")
        table.add_column("Societé", justify="center", style="cyan")
        table.add_column("Date de création", justify="center", style="cyan")

        for pos, client in enumerate(client_list, start=1):
            table.add_row(
                f"{pos}",
                f"{client.full_name}",
                f"{client.email}",
                f"{client.phone}",
                f"{client.commercial_contact.name.upper()} {client.commercial_contact.forname}",
                f"{client.company_name}",
                f"{client.creation_date}",
            )
        self._display.print(table)
        self._display.print("Selectionner un client ou q pour revenir")
        return self._display.input()

    def display_create_client_form(self):
        while True:
            try:
                full_name = self._display.ask("[green]Nom client[/green]")
                email = self._display.ask("[green]Mail de contact[/green]")
                phone = self._display.ask("[green]Telephone[/green]")
                company_name = self._display.ask("[green]Nom de la société[/green]")
                break
            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la creation : {err}")
        return {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "company_name": company_name,
        }

    def display_ask_commercial(self, default_commercial):
        commercial = self._display.ask("[green]Email du commercial en charge[/green]", default=default_commercial)
        return commercial

    def display_update_client_form(self, client_data):
        while True:
            try:
                client_data.full_name = self._display.ask(
                    "[green]Nom du client [/green]", default=client_data.full_name
                )
                client_data.email = self._display.ask("[green]Mail de contact [/green]", default=client_data.email)
                client_data.phone = self._display.ask("[green]Telephone [/green]", default=client_data.phone)
                client_data.company_name = self._display.ask(
                    "[green]Nom de la société[/green]", client_data.company_name
                )
                client_data.commercial_contact = self._display.ask(
                    "[green]Email du commercial en charge[/green]", default=client_data.commercial_contact.email
                )
                break
            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la mise à jour : {err}")
        return client_data

    # -------- Contract views --------------
    def display_create_contract(self, client=None):
        if client:
            default_value = client.full_name
        else:
            default_value = None

        while True:
            try:
                client_full_name = self._display.ask("[green]Nom client[/green]", default=default_value)
                total_amount = self._display.ask("[green]Montant global[/green]")
                remaining_amount = self._display.ask("[green]Montant restant[/green]")

                for pos, item in enumerate(ContractStatus, start=1):
                    self._display.print(f"[green][{pos}] : [/green]{item.value}")
                status_choices = int(self._display.input())
                contract_status = [x for x in ContractStatus][status_choices - 1]
                break
            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la creation : {err}")

        return {
            "client": client_full_name,
            "total_amount": total_amount,
            "remaining_amount": remaining_amount,
            "contract_status": contract_status,
        }

    def display_contract_info(self, contract):
        grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
        grid.add_column(justify="center")
        grid.add_column(justify="center")

        grid.add_row(
            f"[purple]{contract.client.full_name}[/purple]",
            f"[purple]{contract.commercial.name.upper()} {contract.commercial.forname}[/purple]",
        )
        grid.add_row(
            f"[purple]{contract.remaining_amount}/{contract.total_amount}[/purple]",
            "",
        )
        grid.add_row("[green]Date de creation :[/green]", f"[blue]{contract.creation_date}[/blue]")
        grid.add_row(f"[blue]{contract.contract_status.value}[/blue]", "")
        self._display.print(grid)
        os.system("pause")

    def display_list_contract(self, contract_list):
        table = Table(title="Contrats")
        table.add_column("Id", justify="center", style="red")
        table.add_column("Client", justify="center", style="cyan")
        table.add_column("Société", justify="center")
        table.add_column("Commercial", justify="center")
        table.add_column("Somme restante", justify="center", style="red")
        table.add_column("Date création", justify="center", style="cyan")
        table.add_column("Statut", justify="center", style="cyan")

        for pos, contract in enumerate(contract_list, start=1):
            if contract.contract_status == ContractStatus.SIGNED:
                status_color = "green"
            else:
                status_color = "red"

            table.add_row(
                f"{pos}",
                f"[purple]{contract.client.full_name}[/purple]",
                f"[purple]{contract.client.company_name}",
                f"[purple]{contract.commercial.name.upper()} {contract.commercial.forname}[/purple]",
                f"[red]{contract.remaining_amount}[/red]/[purple]{contract.total_amount}[/purple]",
                f"[blue]{contract.creation_date}[/blue]",
                f"[{status_color}]{contract.contract_status.value}[/{status_color}]",
            )

        self._display.print(table)
        self._display.print("Selectionner un contrat ou q pour revenir")
        return self._display.input()

    def display_contract_header(self, contract):
        client = contract.client
        commercial = contract.commercial

        if contract.contract_status == ContractStatus.SIGNED:
            statut_color = "green"
        else:
            statut_color = "light red"

        grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
        grid.add_column(justify="center")
        grid.add_column(justify="center")
        grid.add_row(
            f"[purple]{client.full_name}\n{client.email}\n{client.phone}",
            f"[blue]{commercial.name.upper()} {commercial.forname}\n{commercial.email}",
        )
        grid.add_row(
            f"montant : {contract.remaining_amount}/{contract.total_amount}",
            f"[{statut_color}]{contract.contract_status.value}[/{statut_color}]",
        )
        self._display.print(grid)

    def display_update_contract_form(self, contract, client_fullname, commercial_email):
        while True:
            try:
                self._display.print(f"[green]Nom du client [/green] : {client_fullname}")
                self._display.print(f"[green]Mail commercial [/green] : {commercial_email}")
                contract.total_amount = self._display.ask(
                    "[green]Montant total [/green]", default=contract.total_amount, int=True
                )
                contract.remaining_amount = self._display.ask(
                    "[green]Montant restant [/green]", default=contract.remaining_amount, int=True
                )

                for pos, item in enumerate(ContractStatus, start=1):
                    if item == contract.contract_status:
                        default_pos = pos
                    self._display.print(f"[red][{pos}] : [/red]{item.value}")
                dpt_choices = self._display.ask(
                    f"[green]Statut du contrat [/green][cyan b]{contract.contract_status.value}[/cyan bold]",
                    default=default_pos,
                    int=True,
                )
                contract.contract_status = [x for x in ContractStatus][dpt_choices - 1]
                break
            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la mise à jour : {err}")

        return contract

    # ------------------- Event display -----------------------
    def display_event_header(self, event):
        client = event.client
        if event.contact_support:
            support_name = f"[blue]{event.contact_support.name.upper()} {event.contact_support.forname}[/blue]"
        else:
            support_name = f"[red]Sans responsable[/red]"

        grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
        grid.add_column(justify="center")
        grid.add_column(justify="center")
        grid.add_row("")
        grid.add_row(f"{client.full_name}", f"{client.email}\n{client.phone}")
        grid.add_row(f"[purple]Début :[/purple]", f"{event.event_date_start}")
        grid.add_row(f"[purple]Fin :[/purple]", f"{event.event_date_end}")
        grid.add_row(f"[purple]Contact support :[/purple]", f"{support_name}")
        grid.add_row("")
        self._display.print(grid)

    def display_event_info(self, event):
        if event.contact_support:
            support_name = f"[blue]{event.contact_support.name.upper()} {event.contact_support.forname}[/blue]"
        else:
            support_name = f"[red]Sans responsable[/red]"

        grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
        grid.add_column(justify="left", style="green")
        grid.add_column(justify="center")
        grid.add_row("id", f"{event.id}")
        grid.add_row(None, f"{event.name}")
        grid.add_row(f"{event.client.full_name}", f"{event.client.email}\n{event.client.phone}")
        grid.add_row(f"id : {event.contract.id}", f"{event.contract.contract_status.value}")
        grid.add_row("Date début", f"{event.event_date_start}")
        grid.add_row("Date fin", f"{event.event_date_end}")
        grid.add_row("Contact support", f"{support_name}")
        grid.add_row("Lieu", f"{event.location}")
        grid.add_row("Nombre participant", f"{event.attendees}")
        grid.add_row("Notes", f"{event.note}")
        self._display.print(grid)
        os.system("pause")

    def display_list_event(self, event_list):
        table = Table(title="Evenement")
        table.add_column("Id", justify="center", style="red")
        table.add_column("Client", justify="center", style="cyan")
        table.add_column("Date début", justify="center")
        table.add_column("Date fin", justify="center")
        table.add_column("Contact support", justify="center", style="red")
        table.add_column("Lieu", justify="center", style="cyan")
        table.add_column("Nombre participant", justify="center", style="cyan")

        for pos, event in enumerate(event_list, start=1):
            if event.contact_support:
                support_name = f"[blue]{event.contact_support.name.upper()} {event.contact_support.forname}[/blue]"
            else:
                support_name = f"[red]Sans responsable[/red]"

            table.add_row(
                f"{pos}",
                f"[purple]{event.client.full_name}",
                f"[purple]{event.event_date_start}[/purple]",
                f"[purple]{event.event_date_end}[/purple]",
                f"{support_name}",
                f"{event.location}",
                f"[purple]{event.attendees}[/purple]",
            )

        self._display.print(table)
        self._display.print("Selectionner un evenement ou q pour revenir")
        return self._display.input()

    def display_create_event(self, contract):
        while True:
            try:
                grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
                grid.add_column(justify="center")
                grid.add_column(justify="center")
                grid.add_row("id contrat", f"{contract.id}")
                grid.add_row(f"{contract.client.full_name}", f"{contract.client.email}\n{contract.client.phone}")
                name = self._display.ask("[green]Nom[/green]")
                event_date_start = self._display.ask(f"[green]Date et heure de début[/green] - [red]{DT_STRING}[/red]")
                event_date_start = datetime.strptime(event_date_start, DT_STRING)
                event_date_end = self._display.ask(f"[green]Date et heure de fin[/green] - [red]{DT_STRING}[/red]")
                event_date_end = datetime.strptime(event_date_end, DT_STRING)
                location = self._display.ask("[green]lieu[/green]")
                attendees = self._display.ask("[green]Nombres de participant[/green]")
                attendees = int(attendees)
                note = self._display.ask("[green]Note additionnelle[/green]")
                break

            except ValueError as err:
                self.clear()
                self.display_error_msg("La valeur introduite n'est pas conforme")

            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la creation : {err}")

        return {
            "name": name,
            "event_date_start": event_date_start,
            "event_date_end": event_date_end,
            "location": location,
            "attendees": attendees,
            "note": note,
        }

    def display_event_update(self, event):
        while True:
            try:
                grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
                grid.add_column(justify="center")
                grid.add_column(justify="center")
                event.name = self._display.ask("[green]Nom[/green]", default=event.name)
                event_date_start = self._display.ask("[green]Date début[/green]", default=event.event_date_start)
                event.event_date_start = datetime.strptime(event_date_start, DT_STRING)
                event_date_end = self._display.ask("[green]Date de fin[/green]", default=event.event_date_end)
                event.event_date_end = datetime.strptime(event_date_end, DT_STRING)
                event.location = self._display.ask("[green]lieu[/green]", default=event.location)
                attendees = self._display.ask("[green]Nombres de participant[/green]", dafault=event.attendees)
                event.attendees = int(attendees)
                event.note = self._display.ask("[green]Note additionnelle[/green]", default=event.note)
                break
            except ValueError as err:
                self.clear()
                self.display_error_msg("La valeur introduite n'est pas conforme")

            except Exception as err:
                self.clear()
                self.display_error_msg(f"erreur lors de la mise à jour : {err}")
        return event

    def display_event_define_support(self, event):
        if event.contact_support:
            support_email = event.contact_support.email
        else:
            support_email = None

        grid = Table.grid(expand=False, padding=(0, 1, 1, 1))
        grid.add_column(justify="center", color="green")
        grid.add_column(justify="center")
        grid.add_row("id", f"{event.id}")
        grid.add_row(None, f"{event.name}")
        grid.add_row(f"{event.client.full_name}", f"{event.client.email}\n{event.client.phone}")
        grid.add_row(f"id : {event.contract.id}", f"{event.contract.status}")
        grid.add_row("Date début", f"{event.event_date_start}")
        grid.add_row("Date fin", f"{event.event_date_end}")
        grid.add_row("Lieu", f"{event.location}")
        grid.add_row("Nombre participant", f"{event.attendees}")
        grid.add_row("Notes", f"{event.note}")
        self._display.print(grid)

        support_email = self._display.ask("email du contact support", default=support_email)
        return support_email
