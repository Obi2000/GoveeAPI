# format- "device-name": "device-address"
devices = {"led":"11:22:33:44:55:66"
}
device_modes = ['set','on','off','strobe','diy']
device_names = list(devices.keys())
music_modes=['Energic','Spectrum','Rolling','Rhythm']
scene_modes=['Sunrise','Sunset','Movie','Dating','Romantic','Blinking','Candlelight','Snowflake']
addr_dev_dict = {v:k for k,v in devices.items()}
handle = 21
handle_hex = "0x{:04x}".format(handle)
keepalive ="aa010000000000000000000000000000000000ab"
server_secret = ""
server_port = 5000
