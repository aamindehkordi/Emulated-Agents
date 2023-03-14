import gui.gui as gui
import tkinter as tk

def main():
    """
    Main function.
    """
    # Compress videos
    #cleanup.compress_mov_files('./data/preprocessed/text/allUpdates', './data/processed/videos/all_updates')
    
    # Transcribe videos
    #process.transcribe_updates("data/processed/videos/all_updates", "data/preprocessed/text/all_updates")
    
    # create GUI instance
    root = tk.Tk()
    chatroom = gui.ChatroomGUI(root)
    chatroom.run()
        
if __name__ == "__main__":
    main()
