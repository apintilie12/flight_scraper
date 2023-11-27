from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
from font_fredoka_one import FredokaOne

def setup_inky() -> dict:
	inky_display = InkyPHAT("black")
	inky_display.set_border(inky_display.WHITE)

	wd = inky_display.WIDTH
	hg = inky_display.HEIGHT

	font = ImageFont.truetype(FredokaOne, 18)
	inky = {
		"display" : inky_display,
		"width" : wd,
		"height" : hg,
		"font" : font
	}
	return inky 


def update_inky(flight: dict, inky: dict):
	#flight:  0      1      2      3
	#		fl_no  origin  time  status

	#inky:    0      1      2       3 
	#	   display  width  height  font

	img = Image.new("P", (inky["width"], inky["height"]))
	draw = ImageDraw.Draw(img)
	if flight is not None:
		msg = "Next arriving flight is:"
		w, h = inky["font"].getsize(msg)
		x = 10 
		y = 10
		draw.text((x, y), msg, inky["display"].BLACK, inky["font"])

		msg = flight["fl_no"] + ' ' + flight["origin"]
		x = 10
		y = 10 + h + 10
		draw.text((x, y), msg, inky["display"].BLACK, inky["font"])

		msg = flight["status"] 
		x = 10
		y = 10 + h + 10 + h
		draw.text((x, y), msg, inky["display"].BLACK, inky["font"])
	else:
		msg = "Error occurred!"
		w, h = inky["font"].getsize(msg)
		x = wd / 2 - w / 2
		y = hg / 2 - h / 2
		draw.text((x, y), msg, inky["display"].BLACK, inky["font"])

	inky["display"].set_image(img)
	inky["display"].show()


