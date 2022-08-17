#place all imports here
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import board
import digitalio
import time

###
# MAC OS CODE 
###

# Buttons enter here
# Current call
button1 = digitalio.DigitalInOut(board.GP0)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

# Deafen button
button2 = digitalio.DigitalInOut(board.GP1)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

# Pinned Messages Button
button3 = digitalio.DigitalInOut(board.GP2)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

# Unread Channels
button4 = digitalio.DigitalInOut(board.GP3)
button4.direction = digitalio.Direction.INPUT
button4.pull = digitalio.Pull.UP

#Code button 
button5 = digitalio.DigitalInOut(board.GP4)
button5.direction = digitalio.Direction.INPUT
button5.pull = digitalio.Pull.UP


kbd = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(kbd)

#unread inbox popout
button6 = digitalio.DigitalInOut(board.GP5)
button6.direction = digitalio.Direction.INPUT
button6.pull = digitalio.Pull.UP

#Button Presses

while True:
    # Navigate to current call funtionallity
        if not button1.value:
            print('button two pressed')
            kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.OPTION, Keycode.V)
    #Deafen
        # if not button2.value:
        #     print('button two pressed')
        #     kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.D)
        
    #Upload FIle
        if not button2.value:
            print('button two pressed')
            kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.U)
        
        # View pinned messages (modal)
        if not button3.value:
            print('button three pressed')
            kbd.send(Keycode.COMMAND, Keycode.P)
        
        # Navigate unread channels
        if not button4.value: 
            print("button 4 clicked")
            kbd.send(Keycode.OPTION, Keycode.SHIFT, Keycode.DOWN_ARROW)
        
        if not button5.value:
            print("button five pressed")
            kbd.send(Keycode.COMMAND, Keycode.I)
        
        if not button6.value:
            button6Count = 0
            print("Button 6 has just been pressed")
            while button6Count < 6: 
                kbd.send(Keycode.GRAVE_ACCENT)
                button6Count = button6Count +1
                if button6Count == 3:
                    kbd.send(Keycode.ENTER)
                    kbd.send(Keycode.ENTER)
                if button6Count == 6:
                    kbd.send(Keycode.UP_ARROW)
                    keyboard_layout.write("Kom ons speel RocketLeague")
                    kbd.send(Keycode.DOWN_ARROW)
                    kbd.send(Keycode.ENTER)
                    kbd.send(Keycode.ENTER)

        time.sleep(0.3)
        kbd.release_all()
        
        
###
# WINDOWS CODE
###
