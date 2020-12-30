import os

import requests
import json
import click

__author__ = "jack-txt"


class Context(object):
    def __init__(self, devices, key):
        self.devices = devices
        self.apiKey = key


@click.group()
@click.pass_context
def main(ctx):
    """
    Govee API
    Project Source: https://github.com/jack-txt/govee-api
    """

    key = os.environ.get('GOVEE_KEY')

    # Make a request to Govee asking for devices
    url = 'https://developer-api.govee.com/v1/devices'
    headers = {'Govee-API-Key': key}
    r = requests.get(url, headers=headers)

    ctx.obj = Context(json.loads(r.content)["data"]["devices"], key)


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
    Turn a device on or off.
    """

    safe = True

    try:
        deviceID = ctx.devices[int(iid)]["device"]
        model = ctx.devices[int(iid)]["model"]
    except IndexError:
        print("Couldn't find device " + iid + ", run listdevices to see the devices on your account.")
        safe = False

    if str(state) != "on" and str(state) != "off" and safe:
        print(state + " is not valid! [on/off]")
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "turn", "value": "' + state + '"}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
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
        print("Couldn't find device " + iid + ", run listdevices to see the devices on your account.")
        safe = False

    if not 0 < int(value) <= 100 and safe:
        print(value + " must be a whole number and between 0 and 100")
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "brightness", "value": ' + value + '}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
            click.echo("Device with iid " + str(iid) + " (" + model + ") was set to " + value + "% brightness")
        else:
            click.echo("There was an error while attempting to set brightness on device " + str(
                iid) + " to " + value + "% [Error code: " + str(r.status_code) + "]")


@main.command()
@click.argument("iid", metavar='<iid>')
@click.argument("hexadec", metavar='<hexadec>')
@click.pass_obj
def color(ctx, iid, hexadec):
    """
    Change the color of a device
    """

    safe = True

    try:
        deviceID = ctx.devices[int(iid)]["device"]
        model = ctx.devices[int(iid)]["model"]
    except IndexError:
        print("Couldn't find device " + iid + ", run listdevices to see the devices on your account.")
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
        print("Please enter a valid hexadecimal string, in format #RRGGBB")
        safe = False

    try:
        green = str(int(colors[1], 16))
    except ValueError:
        print("Please enter a valid hexadecimal string, in format #RRGGBB")
        safe = False

    try:
        blue = str(int(colors[2], 16))
    except ValueError:
        print("Please enter a valid hexadecimal string, in format #RRGGBB")
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "color", "value":{"r": ' + red + ', "g": ' + green + ', "b": ' + blue + '}}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
            click.echo("Device with iid " + str(iid) + " (" + model + ") was set to color to " + hexadec_in)
        else:
            click.echo("There was an error while attempting to set color on device " + str(
                iid) + " to " + hexadec + " [Error code: " + str(r.status_code) + "]")


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
        print("Couldn't find device " + iid + ", run listdevices to see the devices on your account.")
        safe = False

    if not 2000 <= int(value) <= 9000 and safe:
        print(value + " must be a whole number and between 2000 and 9000")
        safe = False

    if safe:
        # Contact Govee with the requested device and state
        url = 'https://developer-api.govee.com/v1/devices/control'
        headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
        jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "colorTem", "value": ' + value + '}} '
        r = requests.put(url, data=jsonToSend, headers=headers)

        if r.status_code == 200:
            click.echo("Device with iid " + str(iid) + " (" + model + ") was set to temperature value " + value)
        else:
            click.echo("There was an error while attempting to set temperature value on device " + str(
                iid) + " to " + value + " [Error code: " + str(r.status_code) + "]")


if __name__ == "__main__":
    main()
