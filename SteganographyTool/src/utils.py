import datetime
import time
from functools import wraps
from typing import *

def text_to_bits(text: str, loglimit: int) -> str:
    bits_len = format(len(text),'016b')
    bits_len = bits_len[16-loglimit:]
    return bits_len + ''.join(format(ord(char),'016b') for char in text)

def change_bit(arg: int, bit: int) -> int:
    return (arg//2)*2 + bit

def bits_to_text(bits: str, loglimit: int) -> str:
    return ''.join(chr(int(bits[i:i+16], 2)) for i in range(loglimit, len(bits), 16))

def timer(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res=func(*args, **kwargs)
        end = time.time()
        wrapper.time_taken = end - start
        return res
    wrapper.time_taken=0
    return wrapper