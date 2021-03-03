from random import randint
import time
import pexpect
import signal
import sys
from constants import *

gatt = pexpect.spawn('gatttool -I')
def exit_gracefully(sig, other):
    gatt.sendline("disconnect")
    gatt.sendline("quit")
    sys.exit(1)
signal.signal(signal.SIGINT, exit_gracefully)
def int_to_hex(intv):
    h = hex(intv).replace("0x", "")
    while len(h) < 2:
        h = "0" + h
    return h

def hex_to_rgb(hex):
	hex = hex.lstrip('#')
	hlen = len(hex)
	return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))
		
def get_on():
    sig = (51 ^ 1 ^ 1)
    bins = [51, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_off():
    sig = (51 ^ 1)
    bins = [51, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)

def get_ct_hex(ct):
	#find value in table containing 142 values (2000-9050)
	if ct<2000: ct=2000
	if ct>9050: ct=9050
	CTidx=int((ct-2000)/50)
	r, g, b = hex_to_rgb(CT_Table[CTidx])
	CT1, CT2 = divmod(ct, 0x100)
	bins = [51, 5, 0x0b, r, g, b, CT1, CT2, 0xff, 0x7f, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	sig = checksum(bins)
	bins[19] = sig
	bins_str = map(int_to_hex, bins)
	return "".join(bins_str)

def get_rgb_hex(r,g,b):
    #sig = (51) ^ (5) ^ (0x0b) ^ r ^ g ^ b ^ (0xff)^ (0x7f)
    bins = [51, 5, 0x0b, r, g, b, 0, 0, 0xff, 0x7f, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sig = checksum(bins)
    bins[19] = sig
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_brightness_hex(bright):
    bright = round((bright*255/100)) # converted to a percentage instead of value to 255.
    sig = (51) ^ (4) ^ bright
    bins = [51, 4, bright, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_music_mode(music,r,g,b):
    if music == "Energic":
        musicnum = 0
        r,g,b = 0, 0, 0
    elif music== "Spectrum":
        musicnum = 3
    elif music== "Rolling":
        musicnum = 2
    else:
        musicnum = 5
        r,g,b =0, 0, 0
    musicmode = 0
    bins = [51, 5, 0x0c, musicnum,0x63, musicmode, r, g, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sig = checksum(bins)
    bins[19] = sig
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)

def get_video_mode(area="Part",mode="Game",opSat=100):
	opArea = 0x00
	opMode = 0x01
	
	if area == "All":
		opArea = 0x01
	if mode == "Movie":
		opMode = 0x00
		
	bins = [51, 5, 0x00, opArea, opMode, opSat,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	sig = checksum(bins)
	bins[19] = sig
	bins_str = map(int_to_hex, bins)
	return "".join(bins_str)

def get_scene(scene):
    if scene == "Sunrise":
        scenenum = 0
    elif scene == "Sunset":
        scenenum = 1
    elif scene == "Movie":
        scenenum = 4
    elif scene == "Dating":
        scenenum = 5
    elif scene == "Romantic":
        scenenum = 7
    elif scene == "Blinking":
        scenenum = 8
    elif scene == "Candlelight":
        scenenum = 9
    else:
        scenenum = 15
    sig = ((51)^(5)^(4)^scenenum)
    bins = [51, 5, 4, scenenum, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)

def write_data(data, addr):
    gatt.sendline(f"connect {addr}")
    try:
        gatt.expect("Connection successful", timeout=5)
    except pexpect.exceptions.TIMEOUT:
        dev = addr_dev_dict[addr]
        print(f"Failed to connect to {dev} {addr}")
        return

    #gatt.sendline(f"char-write-req {handle_hex} {keepalive}")
    gatt.sendline(f"char-write-req {handle_hex} {data}")
    gatt.expect(".*")
    gatt.sendline("disconnect")
    gatt.expect(".*")
def turn_on(addr):
    hexstr = get_on()
    write_data(hexstr,addr)
    print(f"Turned {addr_dev_dict[addr]} On")
def turn_off(addr):
    hexstr = get_off()
    write_data(hexstr,addr)
    print(f"Turned {addr_dev_dict[addr]} Off")
def change_color(rgbt, addr):
    r, g, b = rgbt
    hexstr = get_rgb_hex(r,g,b)
    print(hexstr)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} color to {rgbt}")
	
def change_ct(ct, addr):
    hexstr = get_ct_hex(ct)
    print(hexstr)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} color temperature to {ct}")

def change_brightness(bright, addr):
    hexstr = get_brightness_hex(bright)
    print(hexstr)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} brightness to {bright}%")
def change_music(music, rgbt, addr):
    r, g, b = rgbt
    hexstr = get_music_mode(music,r,g,b)
    print(hexstr)
    write_data(hexstr, addr)
    if music=="Energic" or music=="Rhythm":
        print(f"Changed {addr_dev_dict[addr]} Music mode to {music}")
    else:
        print(f"Changed {addr_dev_dict[addr]} Music mode to {music} and Color to {rgbt}")
def change_scene(scene, addr):
    hexstr = get_scene(scene)
    print(hexstr)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} Scene to {scene}")

def change_video(video, addr):
	print(video)
	area=""
	mode=""
	sat="100"
	numArgs = len(video)
	if numArgs>0: area=video[0]
	if numArgs>1: mode=video[1]
	if numArgs>2: sat=video[2]
	opSat = int(sat,0)
	hexstr = get_video_mode(area,mode,opSat)
	print(hexstr)
	write_data(hexstr, addr)
	print(f"Changed {addr_dev_dict[addr]} Video Mode to {video}")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def change_color_all(rgbt):
    for addr in devices.values():
        change_color(rgbt, addr)
def change_brightness_both(bright):
    for addr in devices.values():
        change_brightness(bright, addr)
def gen_rand_color():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    max_c = max([r,g,b])
    factor = 255/max_c
    rp = round(r*factor)
    gp = round(g*factor)
    bp = round(b*factor)
    rgbt = (rp, gp, bp)
    return rgbt

def checksum(data):
	xor=0x00
	for op in data:
		xor^=op
	return xor