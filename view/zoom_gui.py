"""
This module provides the ZoomGUI class, which displays a Zoom-style chatbot interface.

Classes in this module include:
- ZoomGUI: Displays a Zoom-style chatbot interface and handles user input.

EVERYTHING BELOW IS TEMPORARY for now
"""


import pygame
import view.base_gui as gui
class ZoomGUI(gui.BaseGUI):
    def __init__(self, master):
        super().__init__(master)
        # Create a grid layout for video feeds


    def update_video_feed(self, user, video):
        """
        Updates the video feed for the specified user.
        
        Args:
            user (str): The user whose video feed needs to be updated.
            video (bytes): The input video as bytes.
        """
        pass

    def play_audio(self, user, audio):
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
