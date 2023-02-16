import asyncio
import logging
import sys
from customtkinter import *

from .pages import update_page
from ..libs import lib

# Appearance modes
DARK_MODE = "Dark"
LIGHT_MODE = "Light"
SYSTEM_MODE = "System"

# Color themes
BLUE_THEME = "blue"
GREEN_THEME = "green"
DARK_BLUE_THEME = "dark-blue"

set_appearance_mode(DARK_MODE)
set_default_color_theme(BLUE_THEME)


class App(CTk):
    WIDTH: int = 700
    HEIGHT: int = 400

    def __init__(self) -> None:
        super().__init__()

        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.title(lib.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.setup_close_handler()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = CTkLabel(master=self,
                                    text=lib.APP_NAME,
                                    font=("Roboto Medium", -16),
                                    )
        self.title_label.grid(row=0, column=0, pady=5, padx=10)

        self.frame = update_page.UpdatePage(self, self, self.loop)
        self.frame.grid(row=1, sticky="nswe", padx=20, pady=20)

    def setup_close_handler(self) -> None:
        self.protocol("WM_DELETE_WINDOW", self.handle_close)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.handle_close)
            self.bind("<Command-w>", self.handle_close)
            self.createcommand('tk::mac::Quit', self.handle_close)

    def handle_close(self) -> None:
        try:
            future = asyncio.ensure_future(self.close())
            self.loop.run_until_complete(future)
        except RuntimeError as e:
            logging.exception(e)

    async def close(self) -> None:
        self.loop.stop()
        self.destroy()

    def start(self) -> None:
        self.mainloop()
