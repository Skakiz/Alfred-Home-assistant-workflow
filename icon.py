import sys

def getIcon(icon, color):

	result = '';

	if icon == 'mdi:home' :
		result = './icons/home-assistant-icon-' + color + '.png'
	elif icon == 'mdi:alarm' :
		result = './icons/alarm-' + color + '.png'
	elif icon == 'mdi:run-fast' :
		result = './icons/run-fast-' + color + '.png'
	elif icon == 'mdi:remote' :
		result = './icons/remote-' + color + '.png'
	elif icon == 'mdi:compass' :
		result = './icons/compass-' + color + '.png'
	elif icon == 'mdi:thermometer' :
		result = './icons/thermometer-' + color + '.png'
	elif icon == 'light-on' :
		result = './icons/lightbulb-on-' + color + '.png'
	elif icon == 'light-off' :
		result = './icons/lightbulb-' + color + '.png'
	elif icon == 'mdi:cloud' :
		result = './icons/cloud-' + color + '.png'
	elif icon == 'mdi:water-percent' :
		result = './icons/water-percent-' + color + '.png'
	elif icon == 'mdi:weather-rainy' :
		result = './icons/weather-rainy-' + color + '.png'
	elif icon == 'mdi:weather-windy' :
		result = './icons/weather-windy-' + color + '.png'
	elif icon == 'mdi:volume-high' :
		result = './icons/volume-high-' + color + '.png'
	elif icon == 'mdi:battery' :
		result = './icons/battery-' + color + '.png'
	elif icon == 'mdi:wifi' :
		result = './icons/wifi-' + color + '.png'
	elif icon == 'mdi:signal' :
		result = './icons/signal-' + color + '.png'
	elif icon == 'mdi:gauge' :
		result = './icons/gauge-' + color + '.png'
	elif icon == 'home' :
		result = './icons/home-' + color + '.png'
	elif icon == 'away' :
		result = './icons/away-' + color + '.png'
	else :
		result = './icons/home-assistant-icon-' + color + '.png'

	return result;