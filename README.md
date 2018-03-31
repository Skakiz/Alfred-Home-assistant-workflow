# Alfred Home Assistant workflow

This workflow lets you controll your [Home Assistant](https://www.home-assistant.io/) from [Alfred](https://www.alfredapp.com/). 

You will be able to control you lights, get sensor information, trigger automations and look for your devices in device tracker.

## Prerequisites
Home assistant installed and reachable from the computer you run Alfred on. You have to enable to use API password. This is done via the configs.
Alfred 2 or higher

## Setup
You have to provide two settings via alfred command. Just type:

**_haurl** - followed by the address to the home assistant. IE, https://myurl.dnsduck.org:8123. This is stored in the keychain.

**_hapassword** - followed bt the API password. This is stored in the keychain.

## Commands
**hal** (Home assistant lights) You will select the light you want to controll and choose the brithness level of the light. Lights that are unreachable will not be shown.

**haa** (Home assistant autmations) You will select the automation you want to trigger.

**has** (Home assistant sensors) A list with all your sensors that are available.

**had** (Home assistant devices) A list with all devices that the device tracker has found and the latest presence.

## Soon be added
**haal** (Home assistant alarm cotroll) You will be able to control you alarms. Set alarms (homa and away) and disarm the alarm. It will not store your PIN code.

