"""
This module provides the BaseGUI class, a base class for various GUIs in the application.

Classes in this module include:
- BaseGUI: The base class for other GUIs, with common functionality.
"""

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk 

class BaseGUI:
    def __init__(self, master):
        
        self.master = master
        #self.master = ThemedTk(theme="arc")

        # Set color palette
        self.primary_color = "#FFFFFF"  # white
        self.text_color = "#003049"  # black
        self.secondary_color = "#669bbc"  # blue
        self.tertiary_color = "#5B89AE"  # light blue
        self.quaternary_color = "#ADC4D7"  # some sort of blue
        self.quinary_color = "#52688F"  # some sort of blue pt 2
        
        self.main_frame = tk.Frame(self.master, bg=self.primary_color) # Add this line
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.master.title("AI Friend Group")

        # Create main frame
        self.main_frame = tk.Frame(master, bg=self.primary_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create mode selection frame
        self.mode_selection_frame = tk.Frame(master)
        self.mode_selection_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Create mode selection buttons
        self.chat_button = tk.Button(self.mode_selection_frame, text="Chat", bg=self.quaternary_color, fg=self.tertiary_color, font=("Arial", 13), bd=0, command=self.switch_to_chat)
        self.chat_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=8)

        self.zoom_button = tk.Button(self.mode_selection_frame, text="Zoom", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 13), bd=0, command=self.switch_to_zoom)
        self.zoom_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=8)

        self.photobooth_button = tk.Button(self.mode_selection_frame, text="Photobooth", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 13), bd=0, command=self.switch_to_photobooth)
        self.photobooth_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=8)


    def switch_to_chat(self):
        pass  # Implement switching to chat mode

    def switch_to_zoom(self):
        pass  # Implement switching to zoom mode

    def switch_to_photobooth(self):
        pass  # Implement switching to photobooth mode

    def run(self):
        self.master.mainloop()
