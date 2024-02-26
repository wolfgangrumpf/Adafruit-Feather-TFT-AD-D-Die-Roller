# Designed for ESP32-S2 Feather with 240x135 TFT display
# needs .bcf or .pcf fonts

import time
import board
from adafruit_max1704x import MAX17048
import displayio
import terminalio
import digitalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import random

# Set up Battery Monitoring
max17048 = MAX17048(board.I2C())

# Initialize dice
current_die_type = 20
roll_result = ""

# Initialize display
display = board.DISPLAY
splash = displayio.Group()
display.show(splash)

# Initialize Fonts & Colors
font1 = bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf")
font2 = bitmap_font.load_font("/fonts/Dungeon-32.bdf")
font3 = bitmap_font.load_font("/fonts/Dungeon-64.bdf")
font4 = bitmap_font.load_font("/fonts/Dungeon-128.bdf")

red = 0xff2a04
green = 0x199781
yellow = 0xe6ff05

# Create text labels
header_label = label.Label(font2, text="AD&D Die Roller", color=red)
header_label.x = int(display.width / 2 - header_label.width / 2)
header_label.y = 10
splash.append(header_label)

result_label = label.Label(font4, text="", color=yellow)
#result_label.x = int(display.width / 2 - result_label.width / 2)
#result_label.y = int(display.height / 2 - result_label.height / 2)
result_label.x = 125
result_label.y = 75
splash.append(result_label)

type_label = label.Label(font3, text="", color=green)
type_label.x = 12
type_label.y = 75
splash.append(type_label)

batt_label = label.Label(font1, text="BATT: {:} %".format(max17048.cell_percent))
batt_label.x = 1
batt_label.y = 125
splash.append(batt_label)

# Initialize buttons
count_btn = digitalio.DigitalInOut(board.D1)
count_btn.direction = digitalio.Direction.INPUT
count_btn.pull = digitalio.Pull.DOWN

roll_btn = digitalio.DigitalInOut(board.D2)
roll_btn.direction = digitalio.Direction.INPUT
roll_btn.pull = digitalio.Pull.DOWN

select_btn = digitalio.DigitalInOut(board.D0)
select_btn.direction = digitalio.Direction.INPUT
select_btn.pull = digitalio.Pull.UP

# Main loop
while True:
    if not select_btn.value:
        # change die type
        # possible die types are:  4, 6, 8, 10, 12, and 20
        if current_die_type == 20:
            current_die_type = 4
        elif current_die_type == 12:
            current_die_type = 20
        elif current_die_type == 10:
            current_die_type = 12
        elif current_die_type == 8:
            current_die_type = 10
        elif current_die_type == 6:
            current_die_type = 8
        elif current_die_type == 4:
            current_die_type = 6

    if roll_btn.value:
        # Roll a die of the current type
        roll_result = random.randint(1, current_die_type)
    type_label.text = "d{}:".format(current_die_type)
    result_label.text = "{}".format(roll_result)
    display.refresh()
    time.sleep(0.2)


