# What this is.
This a fork of the BLE GoveeAPI for use with Govee Immersion H6199 RGB lighting strips. The H6199 unfortunately has a slightly different format.
I have also added support for H6199 specific features such as the video tracking mode.

# Requirements
This should be done on a Raspberry Pi in whatever room your lights are in. This unfortunately will not work on a Mac/PC (unless you can install [gattlib](https://github.com/labapart/gattlib) on it).

You need to have both python (3.6+) and [gattlib](https://github.com/labapart/gattlib) installed, if it is not already. Gattlib might throw some weird errors during install, but all of the problems I encountered had solutions on StackOverflow. *If you can already run* `gatttool --help` *you do not need to install gattlib.*

For the python requirements, just run
`pip3 install -r requirements.txt`
and you'll have all the required components.

# Recommended Components
I would recommend using homeassistant shell_command API and gatttool, which you can use to create custom workflows with Google Home, Amazon Alexa, etc. If you just want to use the python library without the Smart Home connection & wakeup functionality, you can delete `server.py` and just run through all the files and add in whatever is relevant to you. If you want to integrate this into a smart home, make sure you have a Google Home/Amazon Alexa/some smart assistant that works with IFTTT or gatttool installed.

Also, this is best installed onto a Raspberry Pi, as I said above, both because it is very low profile and because it has gatttool pre-installed. They're also quite cheap and easy to set up!

# Integrating this into a Smart Home
I prefer to run gatttool directly from Home Assistant and the bluetooth coommand because it comes installed in Raspberry pi.
To integrate, set up shell_commands:

    shell_command:
        leds_on: gatttool -i hci0 -b <mac> --char-write-req -a 0x0015 -n 3301010000000000000000000000000000000033
    or
        leds_on: curl http://server_ip:Port/<command>?key=""`

***See [H6199](https://github.com/Obi2000/Govee-H6199-Reverse-Engineering) for list of gatttool commands***

You can also expose your pi (or whatever device you want to control the Govee lights) to the internet and control with http. While there isn't one guide for every single router, you need to log onto your router and find some setting along the lines of "NAT Forwarding." There should be options to add either rules or devices, and click that option.
The external port is the port that gets exposed to the internet, the IP address should be the IP address of the device controlling the Govee lights and the internal port is the port you choose to set the server up on, on the device.

Also, make sure you know your public IP address (which you can find out by Googling "whats my ip address").

Once that is done, go to constants.py and set server_port to whatever you chose your *internal* port to be, and set your server_secret to whatever you can use as a unique identifier. This is just so hackers and tech-savvy friends can't mess with you and strobe your lights or make fake alarms whenever they want.

Then, just go through each of controller.py, tool.py, and server.py and fill in details that are relevant to you or add functionality if you see fit.

## Using IFTTT with Google Home/Amazon Alexa
Once you've installed IFTTT and made an account, create a new applet. The "If" part should be either from Google Assistant or Amazon Alexa depending on what smart device you have, so search it in the toolbar and connect the service. You can choose to have whatever voice command trigger the service, it's up to you! Make sure you use a "$" if you want to arguments in your command like "Wake me up at $" to wake you up at whatever time "$" becomes.

Then the "then that" part should be a webhooks service. The URL should be your public ip with port formatted like "http://URL:PORT/<command>?key=''" with one of "/on" "/off" "/red" or a custom endpoint you put in server.py.

If you add other endpoints to server.py, add them to IFTTT and you'll be all good!

Then, to start up the server, just run `nohup python3 server.py > server_log 2>&1 &` to start up the webserver in the background, and enjoy the control you now posses over your Govee devices!

## How to use server.py and tool.py
Ive built in some standard use cases for the python server including
Once the server is up and running the bluetooth device can be controlled by visiting 
    
    /on?key=""
    /off?key=""
    /red?key=""
    /green?key=""
    /blue?key=""
    /energic?key=""


Custom colors can be controlled with:  0-255
    
    /color/<r>/<g></<b>?key=""

for example red would be

    /color/255/0/0/?key=""

Brightness:  0-100

    /brightness/<brightness%>?key=""

Scenes:  `Sunrise`, `Sunset`, `Movie`, `Dating`, `Romantic`, `Blinking`, `Candlelight`, `Snowflake`
    
    /scenes/<scene>?key=""

Music Mode:  `Energic`, `Spectrum`, `Rolling`, `Rhythm`

    /music/<mode>/<r>/<g>/<b>?key=""

To use tool.py alone, run 
    
    python3 tool.py --help
