# Alfred Home Assistant workflow

This workflow lets you controll your [Home Assistant](https://www.home-assistant.io/) from [Alfred](https://www.alfredapp.com/). 

You will be able to control you lights, get sensor information, trigger automations and look for your devices in device tracker.

## Prerequisites
Home assistant installed and reachable from the computer you run Alfred on. You have to enable to use API password. This is done via the configs.
Alfred 2 or higher

## Setup
You have to provide two settings via alfred command. Just type:

_haurl - followed by the address to the home assistant. IE, https://myurl.dnsduck.org:8123. This is stored in the Mach keychain.

_hapassword - followed bt the API password. This is stored in the Mac keychain.

## Comands
hal - Home assistant lights

haa - Home assistant autmations

has - Home assistant sensors

had - Home assistant devices
