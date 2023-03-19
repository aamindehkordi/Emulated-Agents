"""
This module provides the BaseGUI class, a base class for various GUIs in the application.

Classes in this module include:
- BaseGUI: The base class for other GUIs, with common functionality.
"""

import tkinter as tk

class BaseGUI:
    def __init__(self, master):
        self.master = master
        self.primary_color = "#282c34"
        self.secondary_color = "#4f5b66"
        self.tertiary_color = "#98c379"
        self.text_color = "#abb2bf"

        self.main_frame = tk.Frame(self.master, bg=self.primary_color) # Add this line
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.master.title("AI Friend Group")

        # Set color palette
        self.primary_color = "#fdf0d5"  # cream
        self.text_color = "#003049"  # black
        self.secondary_color = "#669bbc"  # blue
        self.tertiary_color = "#780000"  # red

        # Create main frame
        self.main_frame = tk.Frame(master, bg=self.primary_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create mode selection frame
        self.mode_selection_frame = tk.Frame(master)
        self.mode_selection_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Create mode selection buttons
        self.chat_button = tk.Button(self.mode_selection_frame, text="Chat", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 12), bd=0, command=self.switch_to_chat)
        self.chat_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=8)

        self.zoom_button = tk.Button(self.mode_selection_frame, text="Zoom", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 12), bd=0, command=self.switch_to_zoom)
        self.zoom_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=8)

        self.photobooth_button = tk.Button(self.mode_selection_frame, text="Photobooth", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 12), bd=0, command=self.switch_to_photobooth)
        self.photobooth_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=8)

    def switch_to_chat(self):
        pass  # Implement switching to chat mode

    def switch_to_zoom(self):
        pass  # Implement switching to zoom mode

    def switch_to_photobooth(self):
        pass  # Implement switching to photobooth mode

    def run(self):
        self.master.mainloop()
