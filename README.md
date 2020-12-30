# Govee-API
Manage your Govee connected devices using the command line on your PC! 

## Notice
This software is in no way affiliated with Govee and was created in Python using Govee's Developer API. A personal access token is required to run this project, you can acquire one by going to About Us-> Request API Key in the Govee Home app!

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
