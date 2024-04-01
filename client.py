from fasty import *

@get("/")
def index():
	return "Hello from my very own HTTP framework called Fasty!"

@get("/weather")
def weather():
	return "It's raining."

fasty()

