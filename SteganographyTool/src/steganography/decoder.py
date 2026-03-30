import numpy as np
from typing import *
from src.utils import *
from src.steganography.encoder import Encoder

class Decoder:

    def __init__(self, height: int, width: int, loglimit: int):
        self.height = height
        self.width = width
        self.encoder = Encoder(self.height, self.width, loglimit)
        self.loglimit = loglimit
        self.limit = 1 << loglimit
        self.bits_count=0
    '''
    def set_seed(self, image_array: np.ndarray) -> None:
        bin_seed = ""
        for i in range(16):
            bin_seed += str(image_array[self.height-1,i,0]%2)
        self.encoder = Encoder(self.height, self.width, self.loglimit, int(bin_seed, 2))

    def get_len(self, image_array: np.ndarray) -> int:
        sequence_for_len = self.encoder.generate_sequence(self.loglimit)
        length = 0
        for idx in range(self.loglimit):
            x,y,channel = sequence_for_len[idx]
            image_value = image_array[x,y,channel]
            length += int((image_value % 2)) * pow(2, self.loglimit - 1 - idx)
        return length
    
    @timer
    def decode(self, image_array: np.ndarray) -> str:
        self.set_seed(image_array)
        bits=''
        text_len = self.get_len(image_array)
        sequence = self.encoder.generate_sequence(text_len*16 + self.loglimit)
        for idx in range(text_len * 16 + self.loglimit):
            x,y,channel = sequence[idx]
            image_value=image_array[x,y, channel]
            bits+=str(image_value % 2)
        self.bits_count=len(bits) - 16*16 - self.loglimit
        return bits_to_text(bits, self.loglimit)
    '''

    def get_len(self, image_array: np.ndarray) -> int | None:
        current_bit = 0
        len_binary = ""
        for line in range(0, 512, 4):
            for column in range (0, 512, 4):
                for line_in_block in range(line, line+4):
                    for column_in_block in range(column, column+4):
                        if current_bit < self.loglimit:
                            x = column_in_block + column
                            y = line_in_block + line
                            channel = (line_in_block + column_in_block)%3
                            len_binary += str(image_array[y,x,channel]%2)
                            current_bit += 1
                        else:
                            return int(len_binary,2)

    @timer
    def decode(self, image_array: np.ndarray) -> str | None:
        text_len = self.get_len(image_array)
        if (text_len > 16367 + 16) or (text_len < 17):
            raise NotImplementedError
        text_bits = ""
        current_bit = 0
        self.bits_count = text_len*16 + self.loglimit
        for line in range(0, 512, 4):
            for column in range (0, 512, 4):
                for line_in_block in range(0, 4):
                    for column_in_block in range(0, 4):
                        if current_bit < self.loglimit + text_len*16:
                            x = column_in_block + column
                            y = line_in_block + line
                            channel = (line_in_block + column_in_block) % 3
                            text_bits += str(image_array[y,x,channel]%2)
                            current_bit += 1
                        else:
                            return bits_to_text(text_bits, self.loglimit)


