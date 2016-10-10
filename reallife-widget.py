import pyowm
import os
import random
import datetime
import requests
from escpos import printer

def random_ornament():
	return image_dir+"/ornaments/"+random.choice(os.listdir(image_dir+"/ornaments"))
	
def get_weather_icon( status ):
	return{
		"Clouds": image_dir+"/weather/cloud.jpg",
		"Thunderstorm": image_dir+"/weather/storm-1.jpg",
		"Drizzle": image_dir+"/weather/rain-1.jpg",
		"Rain": image_dir+"/weather/rain.jpg",
		"Snow": image_dir+"/weather/snowing.jpg",
		"Atmosphere": image_dir+"/weather/haze.jpg",
		"Clear": image_dir+"/weather/sun-1.jpg",
		"Extreme": image_dir+"/weather/windy-1.jpg"
	}[status]
	
def get_max_temperature(current_weather):
	return str(current_weather.get_temperature("celsius")["temp_max"])+" C\n"

def get_min_temperature(current_weather):
	return str(current_weather.get_temperature("celsius")["temp_min"])+" C\n"
	
def get_actual_temperature(current_weather):
	return str(current_weather.get_temperature("celsius")["temp"])+" C\n"
	
def print_zodiac_icon(sign):
	p.set(align="center")
	p.image(image_dir+"/zodiac/"+sign+".jpg", impl="bitImageColumn")
	p.text("\n")
	
def print_horoscope(sign):
	response = requests.get("http://widgets.fabulously40.com/horoscope.json?sign="+sign)
	p.text(response.json()["horoscope"]["horoscope"])
	p.text("\n")
	
def print_random_ornament():
	p.set(align="center")
	p.image(random_ornament(), impl="bitImageColumn")
	p.text("\n")
		
image_dir = "/home/nachkonvention/happy/resources/img"

p = printer.File("/dev/usb/lp0")

random_header = random.choice(os.listdir(image_dir+"/hipster"))
random_header_file = image_dir+"/hipster/"+random_header

date = datetime.datetime.now().date().isoformat()

#random_ornament = random.choice(os.listdir(image_dir+"/ornaments"))
#random_ornament_file = image_dir+"/ornaments/"+random_ornament

owm = pyowm.OWM('91642cd9a754ac069409ad7404cc6ce9')
observation = owm.weather_at_place("hamburg")
current = observation.get_weather()
status = current._status
sunrise = datetime.datetime.fromtimestamp(int(current._sunrise_time)).strftime('%H:%M:%S') 
sunset = datetime.datetime.fromtimestamp(int(current._sunset_time)).strftime('%H:%M:%S')

#
#	Greeting
#
p.set(align="center", width=2)
p.text("GOOD MORNIN'!\n");
p.set(align="center")
p.text("What's crackin'?\n")
p.text("\n")

#
#	Header Icon
#
p.set(align="center")
p.image(random_header_file, impl="bitImageColumn")
p.text("\n")

#
#	Datum
#
p.set(align="center", width=2)
p.text("DATUM\n");

p.set(align="center")
p.image(image_dir+"/general/calendar.jpg", impl="bitImageColumn")
p.text("\n")

p.set(align="center", width=2)
p.text(date+"\n")

print_random_ornament()

#
#	Wetter
#
p.set(align="center", width=2)
p.text("WETTER\n");

p.set(align="center")
p.image(get_weather_icon(status), impl="bitImageColumn")

p.set(align="left", width=2)
p.text("AKTUELL\n")
p.set(align="center", width=2)
p.text(get_actual_temperature(current))
p.set(align="left", width=2)
p.text("MAX\n")
p.set(align="center", width=2)
p.text(get_max_temperature(current))
p.set(align="left", width=2)
p.text("MIN\n")
p.set(align="center", width=2)
p.text(get_min_temperature(current))

print_random_ornament()

p.set(align="center", width=2)
p.text("Sonnenaufgang\n")
p.text(sunrise)
p.text("\n\n")
p.text("Sonnenuntergang\n")
p.text(sunset)
p.text("\n")

print_random_ornament()

#
#	Horoskop
#
p.set(align="center", width=2)
p.text("HOROSKOP\n");

print_zodiac_icon("cancer")
print_horoscope("cancer")
print_random_ornament()

p.cut()
