"""
./view/photobooth_gui.py
"""

import cv2
from PIL import Image, ImageTk
import pygame
import view.base_gui as gui

class PhotoboothGUI(gui.BaseGUI):
    
    def __init__(self, master):
        super().__init__(master)
        # Create a live webcam feed widget
        self.video_capture = cv2.VideoCapture(0)
        self.update_live_feed()


    def update_live_feed(self, image):
        """
        Updates the live webcam feed.
        
        Args:
            image (bytes): The input image as bytes.
        """
        # Update the live webcam feed
        _, frame = self.video_capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image)
        self.live_feed.config(image=image)
        self.live_feed.image = image
        self.master.after(10, self.update_live_feed)

    @staticmethod
    def play_audio(user, audio):
        """
        Plays the audio for the specified user.
        
        Args:
            user (str): The user whose audio needs to be played.
            audio (bytes): The input audio as bytes.
        """
        # Play the audio for the specified user
        pygame.mixer.init()
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        