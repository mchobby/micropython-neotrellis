# Detect a "key press" on button 4 to activate/deactivate an output pin (or the user LED). 
# Set the button color in Red/Green accordingly to the output state.
# 
import time
from machine import I2C, Pin
from neotrellis import NeoTrellis

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )
trellis = NeoTrellis(i2c)
trellis.brightness = 0.5
# turn off all LEDs
for i in range(16): 
    trellis.pixels[i] = OFF

# Associate a relay to a PIN (use GP25 for the Onboard LED)
relay = Pin( Pin.board.GP25, Pin.OUT, value=False )
trellis.pixels[4] = RED

# called when button #4 is pressed
def toggle_relay( event ):
    # event.number --> Button
    # event.edge   --> NeoTrellis.EDGE_RISING (pressed), NeoTrellis.EDGE_FALLING
    global relay,trellis
    new_state = not( relay.value() ) # Invert current state
    relay.value( new_state ) # Set the new state
    if new_state==True:
        trellis.pixels[4] = GREEN
    else:
        trellis.pixels[4] = RED


# Attach relay command to button #4 (first button, second line)
#  - Which event to generate on button #4
trellis.activate_key( 4, NeoTrellis.EDGE_RISING ) # button pressed
#  - which function to call for events on button #4
trellis.callbacks[4] = toggle_relay 



while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.02)
