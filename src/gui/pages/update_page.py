from tkinter import messagebox
import webbrowser
from customtkinter import *
import requests

from ...libs import lib
from ...libs.lib import CONFIG_FILE


class UpdatePage(CTkFrame):
    def __init__(self, master, app):
        self.app = app
        super().__init__(master)

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure(0, weight=1)

        self.check_updates_button = CTkButton(
            self,
            text="Controlla aggiornamenti",
            command=self.check_for_updates
        )
        self.check_updates_button.grid(row=0, column=0, padx=20, pady=10)

        self.version = CTkLabel(
            self,
            text="",
            width=150,
            height=45)
        self.version.grid(
            row=1, column=0, columnspan=2, padx=5,)

    def open_github(self):
        url = f'https://api.github.com/repos/{lib.get_key_value_json(CONFIG_FILE, "repo_owner")}/{lib.get_key_value_json(CONFIG_FILE, "repo_name")}/releases/latest'
        webbrowser.open_new_tab(url)

    def check_for_updates(self):

        current_version = lib.get_key_value_json(CONFIG_FILE, "version")

        # Recupera la versione più recente dalla repository su GitHub
        response = requests.get(
            f'https://api.github.com/repos/{lib.get_key_value_json(CONFIG_FILE, "repo_owner")}/{lib.get_key_value_json(CONFIG_FILE, "repo_name")}/releases/latest')
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            print(latest_version)
            if latest_version != current_version:
                self.update_button = CTkButton(
                    self,
                    text="Aggiorna ora",
                    command=lambda: self.update_app(latest_release)
                )
                self.check_updates_button.grid(
                    row=2, column=0, padx=20, pady=10)

        else:
            # Gestione dell'errore
            latest_version = current_version
            messagebox.showerror(
                "Error", "Nessun aggiornamento trovato.")

    def update_app(self, latest_release):
        # Scarica l'aggiornamento dal repository su GitHub
        assets = latest_release['assets']
        for asset in assets:
            if asset['name'].endswith('.exe'):
                url = asset['browser_download_url']
                response = requests.get(url)
                with open('new_version.exe', 'wb') as f:
                    f.write(response.content)

                # Aggiorna il file di configurazione locale con la nuova versione
                lib.update_key_json(CONFIG_FILE, "version",
                                    latest_release['tag_name'])

                # Avvia l'applicazione aggiornata
                os.startfile('new_version.exe')
        self.update_button.destroy()
