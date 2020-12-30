import os
import pathlib

import requests
import json
import click

import contextVars

__author__ = "jack-txt & HarryDev06"


@click.group()
@click.pass_context
def main(ctx):
    """
    Govee API v1.1.0 by jack-txt & HarryDev06

    THIS PRODUCT IS NOT AFFILIATED WITH GOVEE
    """

    key = os.environ.get('GOVEE_KEY')

    # Make a request to Govee asking for devices
    url = 'https://developer-api.govee.com/v1/devices'
    headers = {'Govee-API-Key': key}
    r = requests.get(url, headers=headers)

    ctx.obj = contextVars.Context(json.loads(r.content)["data"]["devices"], key)


@main.command()
def viewlicense():
    "GNU General Public License v3.0"
    f = open(os.path.join(pathlib.Path(__file__).parent.absolute(), "LICENSE"), "r")
    click.echo_via_pager(f.read())


@main.command()
def viewrepo():
    "Open the repo in your browser"
    click.echo("Opening Repository in browser")
    click.launch("https://github.com/jack-txt/govee-api")
    click.echo("Launched")


@main.command()
def giraffe():
    "Prints a giraffe to the screen"
    print("""\

                                           ._ o o
                                           \_`-)|_
                                        ,""       \ 
                                      ,"  ## |   ಠ ಠ. 
                                    ," ##   ,-\__    `.
                                  ,"       /     `--._;)
                                ,"     ## /
                              ,"   ##    /


                        """)


@main.command()
@click.pass_obj
def listdevices(ctx):
    """
    Shows the devices registered to your Govee account
    """

    content = ctx.devices

    # For each device in the users account, display it's details and
    # assign an iid that can be used to access the device
    i = 0
    for device in content:
        print("------------------")
        print("Device iid: " + str(i))
        print("Device MAC: " + device["device"])
        print("Model Name: " + device["model"])
        print("Device Nickname: " + device["deviceName"])
        print("Controllable: " + str(device["controllable"]))
        print("Retrievable: " + str(device["retrievable"]))
        print("Commands: ")
        for commands in device["supportCmds"]:
            print(" " + commands)


@main.command()
@click.argument("iid", metavar='<iid>')
@click.argument("state", metavar='<state>')
@click.pass_obj
def turn(ctx, iid, state):
    """
    Turn a device on or off
    """

    safe = True

    try:
        deviceID = ctx.devices[int(iid)]["device"]
        model = ctx.devices[int(iid)]["model"]
    except IndexError:
        click.echo("Couldn't find device " + iid + ", run listdevices to see the devices on your account.", err=True)
        safe = False

    if str(state) != "on" and str(state) != "off" and safe:
        click.echo(state + " is not valid! [on/off]", err=True)
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "turn", "value": "' + state + '"}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
            click.secho('Success', fg='green', bold=True)
            click.echo("Device with iid " + str(iid) + " (" + model + ") was turned " + state)
        else:
            click.echo(
                "There was an error while attempting to turn device " + str(iid) + " " + state + " [Error code: " + str(
                    r.status_code) + "]")


@main.command()
@click.argument("iid", metavar='<iid>')
@click.argument("value", metavar='<value>', )
@click.pass_obj
def brightness(ctx, iid, value):
    """
    Change the brightness of a device
    """

    safe = True

    try:
        deviceID = ctx.devices[int(iid)]["device"]
        model = ctx.devices[int(iid)]["model"]
    except IndexError:
        click.echo("Couldn't find device " + iid + ", run listdevices to see the devices on your account.", err=True)
        safe = False

    if not 0 < int(value) <= 100 and safe:
        click.echo(value + " must be a whole number and between 0 and 100", err=True)
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "brightness", "value": ' + value + '}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
            click.secho('Success', fg='green', bold=True)
            click.echo("Device with iid " + str(iid) + " (" + model + ") was set to " + value + "% brightness")
        else:
            click.echo("There was an error while attempting to set brightness on device " + str(
                iid) + " to " + value + "% [Error code: " + str(r.status_code) + "]", err=True)


@main.command()
@click.argument("iid", metavar='<iid>')
@click.argument("color", metavar='<color>')
@click.pass_obj
def color(ctx, iid, color):
    """
    Change the color of a device
    """

    if color == "red":
        hexadec = "#ff0000"
    elif color == "green":
        hexadec = "#00ff00"
    elif color == "blue":
        hexadec = "#0000ff"
    elif color == "purple":
        hexadec = "#B200FF"
    elif color == "orange":
        hexadec = "#FFA200"
    elif color == "skyblue":
        hexadec = "#00E8FF"
    elif color == "lime":
        hexadec = "#4DFF00"
    elif color == "computub":
        hexadec = "#0067f4"
    elif color == "bandev":
        hexadec = "#5E17EB"
    elif color == "buddha-quotes":
        hexadec = "#E80054"
    elif color == "labyrinth":
        hexadec = "#0067f4"
    else:
        hexadec = color

    safe = True

    try:
        deviceID = ctx.devices[int(iid)]["device"]
        model = ctx.devices[int(iid)]["model"]
    except IndexError:
        click.echo("Couldn't find device " + iid + ", run listdevices to see the devices on your account.", err=True)
        safe = False

    hexadec_in = hexadec

    hexadec = hexadec.replace("#", '')
    colors = []
    while hexadec:
        colors.append(hexadec[:2])
        hexadec = hexadec[2:]

    try:
        red = str(int(colors[0], 16))
    except ValueError:
        click.echo("Please enter a valid hexadecimal string, in format #RRGGBB or a color name", err=True)
        safe = False

    try:
        green = str(int(colors[1], 16))
    except ValueError:
        click.echo("Please enter a valid hexadecimal string, in format #RRGGBB or a color name", err=True)
        safe = False

    try:
        blue = str(int(colors[2], 16))
    except ValueError:
        click.echo("Please enter a valid hexadecimal string, in format #RRGGBB or a color name", err=True)
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "color", "value":{"r": ' + red + ', "g": ' + green + ', "b": ' + blue + '}}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
            click.secho('Success', fg='green', bold=True)
            click.echo("Device with iid " + str(iid) + " (" + model + ") was set to color to " + hexadec_in)
        else:
            click.echo("There was an error while attempting to set color on device " + str(
                iid) + " to " + hexadec + " [Error code: " + str(r.status_code) + "]", err=True)


@main.command()
@click.argument("iid", metavar='<iid>')
@click.argument("value", metavar='<value>')
@click.pass_obj
def colortem(ctx, iid, value):
    """
    Change the colour temperature of a device
    """

    safe = True

    try:
        deviceID = ctx.devices[int(iid)]["device"]
        model = ctx.devices[int(iid)]["model"]
    except IndexError:
        click.echo("Couldn't find device " + iid + ", run listdevices to see the devices on your account.", err=True)
        safe = False

    if not 2000 <= int(value) <= 9000 and safe:
        click.echo(value + " must be a whole number and between 2000 and 9000", err=True)
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "colorTem", "value": ' + value + '}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
            click.secho('Success', fg='green', bold=True)
            click.echo("Device with iid " + str(iid) + " (" + model + ") was set to temperature value " + value)
        else:
            click.echo("There was an error while attempting to set temperature value on device " + str(
                iid) + " to " + value + " [Error code: " + str(r.status_code) + "]", err=True)


if __name__ == "__main__":
    main()
