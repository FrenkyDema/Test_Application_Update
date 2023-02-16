import asyncio
import sys
from customtkinter import *

from .pages import update_page
from ..libs import lib

# Modes: "System" (standard), "Dark", "Light"
set_appearance_mode("Dark")

# Themes: "blue" (standard), "green", "dark-blue")
set_default_color_theme("blue")


class App(CTk):
    WIDTH = 700
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.title(lib.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.setup_window_close()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = CTkLabel(master=self,
                                    text=lib.APP_NAME,
                                    font=("Roboto Medium", -16),
                                    )
        self.title_label.grid(row=0, column=0, pady=5, padx=10)

        self.frame = update_page.UpdatePage(self, self, self.loop)
        self.frame.grid(row=1, sticky="nswe", padx=20, pady=20)

    def setup_window_close(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing_wrapper)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing_wrapper)
            self.bind("<Command-w>", self.on_closing_wrapper)
            self.createcommand('tk::mac::Quit', self.on_closing_wrapper)

    def on_closing_wrapper(self):
        if not self.loop.is_closed():
            future = asyncio.ensure_future(self.on_closing())
            self.loop.run_until_complete(future)

    async def on_closing(self, future: asyncio.Future):
        # Cancella tutte le task se c'è un event loop in esecuzione
        if asyncio.get_running_loop():
            tasks = [task for task in asyncio.all_tasks(
            ) if task is not asyncio.current_task()]
            [task.cancel() for task in tasks]

            # Attendi che tutte le task siano state cancellate
            await asyncio.gather(*tasks, return_exceptions=True)

        # Chiudi l'event loop
        if not self.loop.is_closed():
            self.loop.stop()
            self.loop.close()
        future.set_result(None)

    def start(self):
        self.mainloop()
