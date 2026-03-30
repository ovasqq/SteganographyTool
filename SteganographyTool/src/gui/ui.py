import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from src.gui.controller import *

class Main_Window:

    def __init__(self, controller: Controller):
        self.root = tk.Tk()
        self.root.title("Steganography")
        self.root.geometry("1000x800")
        self.controller = controller
        self.create_and_load_ui()
        self.controller.set_window(self)

    def create_and_load_ui(self) -> None:
        self.greeting = tk.Label(text="Welcome to Constructive Steganography tool",font=font.Font(size="15"))
        self.greeting.place(relx=0.2, rely=0.1, anchor="center")


        self.entry_label = tk.Label(text="Enter/get your secret message:", font=font.Font(size="15"))
        self.entry_label.place(relx=0.20, rely=0.18, anchor="center")
        self.entry_message = tk.Entry(width=50, justify="center")
        self.entry_message.place(relx=0.20, rely=0.22, anchor="center")

        self.image_frame = tk.Frame(self.root, width=550, height=550, borderwidth=1, relief="solid")
        self.image_frame.place(relx=0.7, rely=0.50, anchor="center")

        self.hide_button = tk.Button(text="Hide message", height=5, width=30, justify="center", bg="gray", command=self.controller.hide_message_action)
        self.hide_button.place(relx=0.2, rely=0.32, anchor="center")

        self.upload_button = tk.Button(text="Upload image", height=5, width=30, justify="center", bg="gray", command=self.controller.upload_image_action)
        self.upload_button.place(relx=0.2, rely=0.45, anchor="center")

        self.reveal_button = tk.Button(text="Reveal message", height=5, width=30, justify="center", bg="gray", command=self.controller.reveal_message_action)
        self.reveal_button.place(relx=0.2, rely=0.58, anchor="center")

        self.name_label = tk.Label(text="Enter name of your image:", font=font.Font(size="15"))
        self.name_label.place(relx=0.20, rely=0.68, anchor="center")
        self.name_message = tk.Entry(width=50, justify="center")
        self.name_message.place(relx=0.20, rely=0.72, anchor="center")

        self.image_label = tk.Label(self.image_frame, text = "No image")

        self.warning_label = tk.Label(text="No warnings", fg="green", font=font.Font(size=20))
        self.warning_label.place(relx=0.7, rely=0.1, anchor="center")

        self.bits_label = tk.Label(text = "Bits encrypted/decrypted: _", font=font.Font(size=15))
        self.bits_label.place(relx=0.7, rely=0.88, anchor="center")

        self.time_label = tk.Label(text="Time taken: _ seconds", font=font.Font(size=15))
        self.time_label.place(relx=0.7, rely=0.94, anchor="center")

    def display_image(self, image: Image.Image) -> None:
        display = image.copy()
        display.thumbnail((500, 500), Image.Resampling.LANCZOS)

        display = ImageTk.PhotoImage(display)

        self.image_label.configure(image=display,text="")
        self.image_label.image = display
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

    def remove_warnings(self) -> None:
        self.warning_label.configure(text="No warnings", fg="green", font=font.Font(size=20))
        self.warning_label.place(relx=0.7, rely=0.1, anchor="center")

    def show_warning(self, warning_text: str) -> None:
        self.warning_label.configure(text=warning_text, fg="red")
        self.root.after(1000, self.remove_warnings)

    def show_bits(self, count: int) -> None:
        self.bits_label.configure(text=f'Bits encrypted/decrypted: {count}', font=font.Font(size=15))
        self.bits_label.place(relx=0.7, rely=0.88, anchor="center")

    def show_time_taken(self, count: float) -> None:
        count = round(count, 3)
        self.time_label.configure(text=f'Time taken: {count} seconds', font=font.Font(size=15))
        self.time_label.place(relx=0.7, rely=0.94, anchor="center")

    def run(self) -> None:
        self.root.mainloop()
