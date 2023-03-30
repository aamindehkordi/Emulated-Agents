"""
./view/chat_gui.py
This module provides the BaseGUI class, a base class for various GUIs in the application.

Classes in this module include:
- BaseGUI: The base class for other GUIs, with common functionality.
"""
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


class BaseGUI(ThemedTk):
    def __init__(self, controller, theme="equilux", font=("Arial", 12), padx=10, pady=10):
        super().__init__()

        self.controller = controller
        self.theme = theme
        self.font = font
        self.padx = padx
        self.pady = pady

        self.primary_color = "#FFFFFF"  # white
        self.text_color = "#003049"  # black
        self.secondary_color = "#669bbc"  # blue
        self.tertiary_color = "#5B89AE"  # light blue
        self.quaternary_color = "#ADC4D7"  # some sort of blue
        self.quinary_color = "#52688F"  # some sort of blue pt 2

        self.set_theme(self.theme)
        self.title("AI Friends App")
        self.geometry("1500x750")

        self.create_menu_bar()
        self.create_main_frame()

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Settings", command=self.settings)
        menu_bar.add_cascade(label="Options", menu=options_menu)

    def settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("400x300")

        label_theme = tk.Label(settings_window, text="Theme:")
        label_theme.grid(row=0, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)

        theme_var = tk.StringVar()
        theme_var.set(self.theme)
        theme_option = ttk.Combobox(settings_window, textvariable=theme_var, values=self.get_themes())
        theme_option.grid(row=0, column=1, sticky=tk.W, padx=self.padx, pady=self.pady)

        apply_button = tk.Button(settings_window, text="Apply", command=lambda: self.apply_settings(theme_var.get()))
        apply_button.grid(row=1, column=1, sticky=tk.E, padx=self.padx, pady=self.pady)

    def apply_settings(self, theme):
        self.theme = theme
        self.set_theme(self.theme)

    def create_main_frame(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)

        title = ttk.Label(main_frame, text="AI Friends App", font=("Arial", 24))
        title.pack(pady=(self.pady, 50))

        chat_button = ttk.Button(main_frame, text="Chat Mode", command=self.controller.switch_to_chat_mode)
        chat_button.pack(pady=self.pady, ipadx=50, ipady=20)

        zoom_button = ttk.Button(main_frame, text="Zoom Mode", command=self.controller.switch_to_zoom_mode)
        zoom_button.pack(pady=self.pady, ipadx=50, ipady=20)

        photobooth_button = ttk.Button(main_frame, text="Photobooth Mode",
                                       command=self.controller.switch_to_photobooth_mode)
        photobooth_button.pack(pady=self.pady, ipadx=50, ipady=20)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side=tk.BOTTOM, pady=(50, self.pady))

        help_button = ttk.Button(bottom_frame, text="Help", command=self.show_help)
        help_button.pack(side=tk.RIGHT, padx=self.padx)

        settings_button = ttk.Button(bottom_frame, text="Settings", command=self.settings)
        settings_button.pack(side=tk.RIGHT, padx=self.padx)

    def show_help(self):
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_window.geometry("400x300")

        help_text = "To be implemented"
        help_label = ttk.Label(help_window, text=help_text, wraplength=350)
        help_label.pack(padx=self.padx, pady=self.pady)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    # Example usage
    class DummyController:
        @staticmethod
        def switch_to_chat_mode():
            print("Switching to chat mode")

        @staticmethod
        def switch_to_zoom_mode():
            print("Switching to zoom mode")

        @staticmethod
        def switch_to_photobooth_mode():
            print("Switching to photobooth mode")


    dummy_controller = DummyController()
    base_gui = BaseGUI(dummy_controller)
    base_gui.mainloop()
