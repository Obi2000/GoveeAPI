from flask import Flask, request
import time
import pexpect
from constants import server_secret, server_port
app = Flask(__name__)

console = pexpect.spawn("bash")
#on
@app.route('/on', methods=["GET"])
def on():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --mode on")
        return "done"
    else:
        return "Empty request"
#off
@app.route('/off', methods=["GET"])
def off():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --mode off")
        return "done"
    else:
        return "Empty request"

#brightness
@app.route('/brightness/<bright>', methods=["GET"])
def bright(bright):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --brightness " + bright)
        return "done"
    else:
        return "Empty request"


#color temperature
@app.route('/ct/<temp>', methods=["GET"])
def ct(temp):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --temp " + temp)
        return "done"
    else:
        return "Empty request"
		
#########################################################################################################################################################
@app.route('/alarm', methods=["POST", "GET"])
def alarm():
    if request.method == "POST":
        rdict = request.form.to_dict()
        if "alarm" in rdict.keys():
            alarm = request.form["alarm"].replace(" at ", "").replace(" : ", ":").replace(" . ", ".").replace(" .", ".")
            correct_ampm_alarm = alarm.replace("a.m.", "AM").replace("p.m.", "PM")
            is_day_before = (time.strftime("%p") == "PM")
            time_str = correct_ampm_alarm + " tomorrow" if is_day_before else correct_ampm_alarm
            command_str = f"at {time_str} -f ./start_bright_increase.sh"
            print(command_str)
            console.sendline(command_str)
            return "done"
        else:
            return "Bad request"
    else:
        return "Empty request"
#########################################################################################################################################################
@app.route('/strobe', methods=["GET"])
def strobe():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --mode strobe --period .3")
        return "done"
    else:
        return "Bad request"
#########################################################################################################################################################

#red
@app.route('/red', methods=["GET"])
def red():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --color 255 0 0")
        return "done"
    else:
        return "Empty request"

#green
@app.route('/green', methods=["GET"])
def green():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --color 0 255 0")
        return "done"
    else:
        return "Empty request"

#blue
@app.route('/blue', methods=["GET"])
def blue():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --color 0 0 255")
        return "done"
    else:
        return "Empty request"

#energic
@app.route('/energic', methods=["GET"])
def energic():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --music Energic --color 0 0 0")
        return "done"
    else:
        return "Empty request"
#########################################################################################################################################################
#color
@app.route('/color/<r>/<g>/<b>', methods=["GET"])
def color(r,g,b):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --color " + r + " " + g + " " + b)
        return "done"
    else:
        return "Empty request"

#music
@app.route('/music/<music_mode>/<r>/<g>/<b>', methods=["GET"])
def music(music_mode,r,g,b):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --music " + music_mode + " --color " + r + " " + g + " " + b)
        return "done"
    else:
        return "Empty request"

#scenes
@app.route('/scene/<scene_mode>', methods=["GET"])
def scene(scene_mode):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --scene " + scene_mode  )
        return "done"
    else:
        return "Empty request"


#video
@app.route('/video', methods=["GET"])
def video():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("python3 tool.py --video Part Game 10")
        return "done"
    else:
        return "Empty request"

	
#############################################################################################################################################################################
@app.route('/end_strobe')
def end():
    console.sendintr()
    return "Done"
##########################################################################################################################################################################



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)
