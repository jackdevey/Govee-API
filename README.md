# Govee-API
Manage your Govee connected devices using the command line on your PC! 

## Notice
This software is in no way affiliated with Govee and was created in Python using Govee's Developer API. A personal access token is required to run this project, you can acquire one by going to About Us-> Request API Key in the Govee Home app!

## Example commands
Here is a list of example commands to get you started with Govee-API:

### Query Devices
To find out what devices can be used in this CLI, you can run the command **listdevices**.

```
goveeApi listdevices
```

This should return the following data about each device added to your account:
```
Device iid: Int
Device MAC: Str
Model Name: Str
Device Nickname: Str
Controllable: True
Retrievable: True
Commands: Str[]
```

### Turn Devices On or Off
Devices can be turned on using the **turn** command followed by the iid and the state (on/off)

```
goveeApi turn 0 on
```

This should turn the device with the iid of 0 on

### Change Device Brightness
The brightness of your device can be changed with the **brightness** command followed by iid and the integer value. The value must be between 1 and 100 without a percentage sign (%) after it.

```
goveeApi brightness 0 50
```

This should make the device with the iid of 0 have a brightness of 50%

### Change Device Colour
The colour of your device should be changed using the **color** command followed by the device's iid and the requested colour in a hexadecimal format (#RRGGBB) if you are stuck for colours, you can find some [here](https://htmlcolorcodes.com/) There are a few colours you can also use such as **red**, **green**, **blue**, and **purple** etc.

```
goveeApi color 0 #0067f4
```

This should make the device with the iid of 0 display a blue-ish colour

### Change Device Colour Temperature
The colour temperature of your device should be changed using the **colortem** command followed by the device's iid and the requested colour temperature in an integer format between 2000 and 9000.

```
goveeApi colortem 0 2000
```

This should make the device with the iid of 0 display a warm white colour.

## Installation Guide (v1.0.0)

> This release may be blocked by your anti-virus software, Microsoft Defender marks the software as [Trojan:Win32/Fuerboos.D!cl](https://go.microsoft.com/fwlink/p/?linkid=849967&Name=Trojan:Win32/Fuerboos.D!cl). This issue has been reported to Microsoft, if your antivirus software marks as dangerous too, let me know by creating an issue!

### Step 1

Download the file **goveeApi.exe**. If your anti-virus software marks it as dangerous, disable it and continue.

### Step 2

Move the file from your downloads file to your root directory (on windows this is C:\). *The location doesn't really matter as long as you don't leave it in the downloads folder*

### Step 3 

Add the following to your system environment variables:

a. A variable named `GOVEE_KEY` with the value of your Govee API key
b. Add the install location, to the `Path` variables

### Step 4

Open a command line and run the command `goveeApi` and you should see the help page!
