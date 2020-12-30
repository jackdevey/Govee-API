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
    Govee API by jack_txt. v1.0.0

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
    Devices registered to your Govee Account:
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
@click.argument("iid")
@click.argument("state")
@click.pass_obj
def turn(ctx, iid, state):
    deviceID = ctx.devices[int(iid)]["device"]
    model = ctx.devices[int(iid)]["model"]

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
@click.argument("iid")
@click.argument("value")
@click.pass_obj
def brightness(ctx, iid, value):
    deviceID = ctx.devices[int(iid)]["device"]
    model = ctx.devices[int(iid)]["model"]

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
@click.argument("iid")
@click.argument("hexadec")
@click.pass_obj
def color(ctx, iid, hexadec):
    deviceID = ctx.devices[int(iid)]["device"]
    model = ctx.devices[int(iid)]["model"]

    hexadec = hexadec.replace("#", '')
    colors = []
    while hexadec:
        colors.append(hexadec[:2])
        hexadec = hexadec[2:]

    # Contact Govee with the requested device and state
    url = 'https://developer-api.govee.com/v1/devices/control'
    headers = {'Content-Type': 'application/json', 'Govee-API-Key': ctx.apiKey}
    jsonToSend = '{"device": "' + deviceID + '","model": "' + model + '","cmd": {"name": "color", "value":{"r": ' + str(
        int(colors[0], 16)) + ', "g": ' + str(
        int(colors[1], 16)) + ', "b": ' + str(int(colors[2], 16)) + '}}} '
    r = requests.put(url, data=jsonToSend, headers=headers)

    if r.status_code == 200:
        click.echo("Device with iid " + str(iid) + " (" + model + ") was set to color to " + hexadec)
    else:
        click.echo("There was an error while attempting to set color on device " + str(
            iid) + " to " + hexadec + " [Error code: " + str(r.status_code) + "]")


@main.command()
@click.argument("iid")
@click.argument("value")
@click.pass_obj
def colortem(ctx, iid, value):
    deviceID = ctx.devices[int(iid)]["device"]
    model = ctx.devices[int(iid)]["model"]

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
