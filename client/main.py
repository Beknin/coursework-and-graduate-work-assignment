import tkinter as tk
from gui.login_window import LoginWindow

def main():
    root = tk.Tk()
    root.withdraw()
    login = LoginWindow()
    login.mainloop()

if __name__ == "__main__":
    main()