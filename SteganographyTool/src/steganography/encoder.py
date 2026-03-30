import numpy as np
from typing import *
from src.utils import *
import time

class Encoder:

    def __init__(self, height: int, width: int, loglimit: int, seed = int(time.time()) % 65536):
        self.loglimit = loglimit
        self.limit = 1<<loglimit
        self.seed = seed
        self.height = height
        self.width = width
        self.bits_count=0

    def create_noize(self) -> np.ndarray:
        np.random.seed(self.seed)
        noize_image = np.random.randint(0, 256, (self.height, self.width, 3), dtype=int)
        return noize_image
    '''
    def generate_sequence(self, count:int) -> list:
        np.random.seed(self.seed)
        generated_set = set()
        generated = []
        while len(generated) < count:
            value = (np.random.randint(0,self.height),np.random.randint(0,self.width),np.random.randint(0,3))
            if (value not in generated_set and value[0] < self.height - 1):
                generated_set.add(value)
                generated.append(value)
        return generated
    
    @timer
    def encode(self, text: str) -> np.ndarray:
        self.seed = int(time.time())%65536
        text = "some magic words" + text
        text_bits = text_to_bits(text, self.loglimit)
        self.bits_count = len(text_bits) - 16*16 - self.loglimit
        noized_image = self.create_noize()
        sequence = self.generate_sequence(len(text_bits))

        for idx in range(len(text_bits)):
            x,y,channel = sequence[idx]
            noized_image[x, y, channel]=change_bit(noized_image[x,y,channel], int(text_bits[idx]))

        bin_seed = bin(self.seed)[2:]
        bin_seed = '0'*(16-len(bin_seed))+bin_seed
        for i in range(16):
            noized_image[self.height-1,i,0]=change_bit(noized_image[self.height-1,i,0], int(bin_seed[i]))
        return noized_image
    '''

    @timer
    def encode(self, text: str) -> np.ndarray:
        text = "some magic words" + text
        text_bits = text_to_bits(text, self.loglimit)
        self.bits_count = len(text_bits)
        bits_number = len(text_bits)
        current_bit = 0
        noized_image = self.create_noize()
        for line in range(0, 512, 4):
            for column in range (0, 512, 4):
                for line_in_block in range(0, 4):
                    for column_in_block in range(0, 4):
                        if current_bit < bits_number:
                            x = column_in_block + column
                            y = line_in_block + line
                            channel = (line_in_block + column_in_block)%3
                            noized_image[y,x,channel] = change_bit(noized_image[y,x,channel], int(text_bits[current_bit]))
                            current_bit += 1
                        else:
                            return noized_image
        return noized_image





