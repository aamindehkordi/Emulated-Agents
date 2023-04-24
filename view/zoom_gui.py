"""
./view/zoom_gui.py
"""
import tkinter as tk
from tkinter import ttk
from view.base_gui import BaseGUI


class ZoomGUI(BaseGUI):
    def __init__(
        self, controller, theme="equilux", font=("Arial", 12), padx=10, pady=10
    ):
        super().__init__(controller, theme, font, padx, pady)
        self.geometry("1400x600")
        self.title("AI Friends Zoom Mode")

    def create_main_frame(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)

        grid_frame = ttk.Frame(main_frame)
        grid_frame.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)

        self.create_video_grid(grid_frame)

    def create_video_grid(self, grid_frame):
        for i in range(2):
            for j in range(3):
                placeholder_label = ttk.Label(
                    grid_frame,
                    text=f"Agent Video {i * 3 + j + 1}",
                    relief=tk.RAISED,
                    width=20,
                )
                placeholder_label.grid(row=i, column=j, padx=self.padx, pady=self.pady)
