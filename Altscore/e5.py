import requests

# Radar references #
enemy = "^"
hope = "#"
obst = "$"
empty_space = "0"
line_jump = "|"

# initial enemy pos = 5g
# first turn enemy = 1b
# second turn enemy = 3a
# third turn = 5b

raw_lect = "a01b01c01d01e01f01g01h01|a02b02c02d$2e02f02g02h02|a03b03c$3d03e03f03g03h03|a04b04c$4d04e04f04g04h04|a05b^5c05d05e05f05g05h05|a06b06c06d$6e06f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e#8f08g08h08|"
skip = ["a", "b", "c", "d", "e", "f", "g", "h", "1", "2", "3", "4", "5", "6", "7", "8"]

split_list = raw_lect.split("|")
clean_lect = ""

for line in reversed(split_list):
	clean_lect += line + "|"

radar_screen = ""

for letter in clean_lect:
	if letter == line_jump:
		radar_screen += "\n"
	elif (letter == enemy):
		radar_screen += enemy + " "
	elif (letter == hope):
		radar_screen += hope + " "
	elif (letter == obst):
		radar_screen += obst + " "
	elif (letter in skip):
		continue
	else:
		radar_screen += empty_space + " "

print(radar_screen)

## FOR TESTING PURPOSES ###
# default_screen = """0 0 0 0 0 # 0 0
# 0 0 0 0 0 0 0 0
# 0 0 0 0 $ 0 0 0
# 0 0 0 0 $ 0 ^ 0
# 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 $
# 0 0 0 0 $ 0 0 0
# 0 0 0 0 0 0 0 0"""

# print(default_screen)
