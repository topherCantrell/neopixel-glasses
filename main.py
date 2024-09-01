import machine
import neopixel
import time
import random

neo = neopixel.NeoPixel(machine.Pin(2),48)


# For our mapping, we'll say the four pixels at the bridge (facing the glasses):
#
#        28 O    O 20
#        29 O    O 19
# 
#                                     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
# Left starts at 20 and ends at 19  
# Right starts at 28 and ends at 29  13 12 11 10  9  8  7  6  5  4  3  2  1 23 22 21 20 19 18 17 16 15 14
#                                    24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47

INF_MAP = [ 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23, 0, 1, 2, 3,
           28,27,26,25,24,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29]

COPY_MAP = [20,21,22,23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,
            23,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]

MIRROR_MAP = [4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23, 0, 1, 2, 3,
              4,3,2,1,0,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5]

def get_random(max):
    ret = random.getrandbits(16)
    return ret % max

def get_random_color():
    return [get_random(50),get_random(50),get_random(50)]

def _do_map(data,dst,map):
    i = 0    
    while i<48:
        k = data[map[i]]       
        dst[i] = data[map[i]]
        i += 1    

def infinity_map(data,dst):
     _do_map(data,dst,INF_MAP)

def copy_map(data,dst):
    _do_map(data,dst,COPY_MAP)

def mirror_map(data,dst):
    _do_map(data,dst,MIRROR_MAP)

def sparkle(num):
    for _ in range(num):    
        for i in range(48):
            neo[i] = get_random_color()
        neo.write()
        time.sleep(.1)

def infinity(num):
    for _ in range(num):
        for i in range(48):
            d = [(0,0,0)]*48
            d[i] = (10,10,10)

            infinity_map(d,neo)
            #copy_map(d,neo)
            #mirror_map(d,neo)

            neo.write()
            #time.sleep(1.5)

def fill_wipe(color_start,color_fill,map,ran=24):
    buffer = [color_start]*ran
    for i in range(ran):
        buffer[i] = color_fill
        map(buffer,neo)
        neo.write()
        time.sleep(.05)

def wipes_mirror(num):
    back = (0,0,0)
    for _ in range(num):
        color = get_random_color()
        fill_wipe( back,color,mirror_map)
        back = color

def wipes_copy(num):
    back = (0,0,0)
    for _ in range(num):
        color = get_random_color()
        fill_wipe( back,color,copy_map)
        back = color

def wipes_infinity(num):
    back = (0,0,0)
    for _ in range(num):
        color = get_random_color()
        fill_wipe( back,color,infinity_map,48)
        back = color

def wheel(num):
    color1 = get_random_color()
    color2 = get_random_color()
    color3 = get_random_color()
    color4 = get_random_color()
    buffer = [(0,0,0)] * 24
    for i in range(4):
        buffer[i]= color1
        buffer[i+6] = color2
        buffer[i+12] = color3
        buffer[i+18] = color4
    for _ in range(num):
        mirror_map(buffer,neo)
        neo.write()
        time.sleep(0.1)
        a = buffer[0]
        buffer = buffer[1:]
        buffer.append(a)

def pulse(num):
    color = [0,0,0]
    rc = get_random(3)
    for _ in range(num):
        for i in range(10):
            color[rc] = i
            buf = [color]*24
            copy_map(buf,neo)
            neo.write()
            time.sleep(.05)
        for i in range(9,-1,-1):
            color[rc] = i
            buf = [color]*24
            copy_map(buf,neo)
            neo.write()
            time.sleep(.05)

while True:
    wheel(48)
    pulse(4)
    wipes_mirror(4)
    wipes_copy(4)
    wipes_infinity(2)
    infinity(10)
    sparkle(40)
