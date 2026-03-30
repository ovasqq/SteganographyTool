from PIL import Image
import tkinter as tk

from src.gui.ui import Main_Window
from src.steganography.encoder import *
from src.steganography.decoder import *

class Controller:
    def __init__(self):
        self.window = None
        self.encoder = Encoder(512,512, 16)
        self.decoder = Decoder(512,512, 16)
        self.image_array = None
        self.image = None
        self.text = None

    def set_window(self,window: Main_Window) -> None:
        self.window = window

    def hide_message_calc(self, text: str) -> None:
        self.image_array = self.encoder.encode(text)

    def convert_imagearray_to_image(self) -> None:
        image = Image.fromarray(self.image_array.astype('uint8'),'RGB')
        self.image = image

    def show_image(self) -> None:
        self.window.display_image(self.image)

    def save_image(self) -> None:
        if self.image is None:
            return
        image_to_save = self.image
        name_to_save=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        image_to_save.save("./saves/"+name_to_save+".png")

    def hide_message_action(self) -> None:
        text = self.window.entry_message.get()
        self.window.entry_message.delete(0, tk.END)
        if text == "":
            self.show_warning("No text entered")
            return
        if len(text) > 16367:
            self.show_warning("Text is too long")
            return
        self.hide_message_calc(text)
        self.convert_imagearray_to_image()
        self.show_image()
        self.save_image()
        self.show_bits_encode()
        self.show_time_taken_encode()

    def reveal_message_calc(self, image_array: np.ndarray) -> None:
        self.text = self.decoder.decode(image_array)

    def show_message(self) -> None:
        self.window.entry_message.delete(0, tk.END)
        self.window.entry_message.insert(0,self.text)

    def reveal_message_action(self) -> None:
        try:
            hidden = self.image_array.copy()
        except AttributeError:
            self.show_warning("No image uploaded")
        else:
            width, height = self.image.size
            if (width != 512 or height != 512):
                self.show_warning("Wrong image size, convert to 512x512")
                return
            try:
                self.reveal_message_calc(hidden)
            except NotImplementedError:
                self.show_warning("No hidden message")
            else:
                if self.text[:16] != "some magic words":
                    self.show_warning("No hidden message")
                    return
                self.text = self.text[16:]
                self.show_message()
                self.show_bits_decode()
                self.show_time_taken_decode()

    def get_image_by_name(self) -> None:
        name = self.window.name_message.get()
        path = "to_upload_pics/"+name
        self.image = Image.open(path).convert('RGB')

    def convert_image_to_imagearray(self) -> None:
        self.image_array = np.array(self.image)

    def show_warning(self, text: str) -> None:
        self.window.show_warning(text)

    def upload_image_action(self) -> None:
        try:
            self.get_image_by_name()
        except PermissionError:
            self.show_warning("Permission error")
        except FileNotFoundError:
            self.show_warning("File not found")
        else:
            self.convert_image_to_imagearray()
            self.show_image()

    def show_bits_encode(self) -> None:
        self.window.show_bits(self.encoder.bits_count)

    def show_bits_decode(self) -> None:
        self.window.show_bits(self.decoder.bits_count)

    def show_time_taken_encode(self) -> None:
        self.window.show_time_taken(self.encoder.encode.time_taken)

    def show_time_taken_decode(self) -> None:
        self.window.show_time_taken(self.decoder.decode.time_taken)

