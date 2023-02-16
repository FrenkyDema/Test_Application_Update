import asyncio
from tkinter import messagebox
import aiohttp
import webbrowser
from customtkinter import *
import requests
from PIL import Image, ImageTk, ImageSequence
import os

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
            command=lambda: asyncio.ensure_future(self.check_for_updates())
        )
        self.check_updates_button.grid(row=0, column=0, padx=20, pady=10)

        self.version = CTkLabel(
            self,
            text="",
            width=150,
            height=45)
        self.version.grid(
            row=1, column=0, columnspan=2, padx=5,)

        # Crea un'immagine GIF animata e ottieni il frame iniziale
        self.loading_gif = Image.open(lib.get_image_path('loading.gif'))
        self.loading_gif_frames = [ImageTk.PhotoImage(
            frame) for frame in ImageSequence.Iterator(self.loading_gif)]

    def update_button_state(self, state):
        if state == "loading":
            self.check_updates_button.config(
                text="Caricamento in corso...", state="disabled")
            self.loading_gif_index = 0
            self.animate_loading_gif()
        elif state == "loaded":
            self.check_updates_button.config(
                text="Controlla aggiornamenti", state="normal")
            self.after_cancel(self.loading_gif_animation_id)

    def animate_loading_gif(self):
        self.check_updates_button.config(
            image=self.loading_gif_frames[self.loading_gif_index])
        self.loading_gif_index = (
            self.loading_gif_index + 1) % len(self.loading_gif_frames)
        self.loading_gif_animation_id = self.after(
            100, self.animate_loading_gif)

    async def open_github(self):
        url = f'https://api.github.com/repos/{lib.get_key_value_json(CONFIG_FILE, "repo_owner")}/{lib.get_key_value_json(CONFIG_FILE, "repo_name")}/releases/latest'
        webbrowser.open_new_tab(url)

    async def check_for_updates(self):
        current_version = lib.get_key_value_json(CONFIG_FILE, "version")

        # Disabilita il bottone di aggiornamento e mostra l'icona animata
        self.update_button_state("loading")

        print("check_for_updates")

        # Recupera la versione più recente dalla repository su GitHub
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.github.com/repos/{lib.get_key_value_json(CONFIG_FILE, "repo_owner")}/{lib.get_key_value_json(CONFIG_FILE, "repo_name")}/releases/latest') as response:
                if response.status == 200:
                    latest_release = await response.json()
                    latest_version = latest_release['tag_name']
                    print(latest_version)
                    if latest_version != current_version:
                        self.update_button = CTkButton(
                            self,
                            text="Aggiorna ora",
                            command=lambda: asyncio.ensure_future(
                                self.update_async(latest_release))
                        )
                        self.update_button.grid(
                            row=2, column=0, padx=20, pady=10)

                else:
                    # Gestione dell'errore
                    messagebox.showerror(
                        "Error", "Nessun aggiornamento trovato.")
        # Riabilita il bottone di aggiornamento e nasconde l'icona animata
        self.check_updates_button.config(state='normal')
        self.check_updates_button.config(image='')

    async def update_async(self, latest_release):
        # Scarica l'aggiornamento dal repository su GitHub
        async with aiohttp.ClientSession() as session:
            async with session.get(latest_release['zipball_url']) as response:
                with open('latest_release.zip', 'wb') as f:
                    f.write(await response.read())

        # Aggiorna il file di configurazione locale con la nuova versione
        lib.update_key_json(CONFIG_FILE, "version", latest_release['tag_name'])

        # Avvia l'applicazione aggiornata
        os.startfile('latest_release.zip')
