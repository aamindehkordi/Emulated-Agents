import tools.cleanup as cleanup, tools.process as process, gui.gui as gui
import tkinter as tk

def main():
    """
    Main function.
    """
    # create GUI instance
    root = tk.Tk()
    chatroom = gui.ChatroomGUI(root)
    chatroom.run()
        
if __name__ == "__main__":
    main()
