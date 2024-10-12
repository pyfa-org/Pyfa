import gc
from ctypes import *
from collections import defaultdict
import os
def gdiReport(desc=''):
    PH = windll.kernel32.OpenProcess(0x400, 0, os.getpid())
    numGdi = windll.user32.GetGuiResources(PH, 0)
    windll.kernel32.CloseHandle(PH)
    print (f'{desc}, {numGdi}')


last = None
def output_memory():
    global last
    d = defaultdict(int) 
    for o in gc.get_objects():
        name = type(o).__name__  
        if name == 'Bitmap':
            del o
        d[name] += 1

    items = d.items()
    items = sorted(items,key=lambda x:x[1])
    print('------')
    for key, value in items:
        if last is not None:
            if value -last[key] !=0:
                print(f'{key} {value - last[key]}, {value}')
        else:
            print( key, value)
            
    last = d
