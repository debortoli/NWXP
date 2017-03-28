from Tkinter import Tk, Label, Button

class TKBoard:
    def __init__(self, master,boardlogic):
        self.master = master
        master.title("GRID SIMULATOR")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text=str(boardlogic.level), command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

