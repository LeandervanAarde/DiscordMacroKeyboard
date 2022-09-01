import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import board
import digitalio
import time
import analogio



#upload button top right
button1 = digitalio.DigitalInOut(board.GP0)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

# Code button
button2 = digitalio.DigitalInOut(board.GP1)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

# Unread Channels  Button
button3 = digitalio.DigitalInOut(board.GP2)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

# Pinned messages Channels
button4 = digitalio.DigitalInOut(board.GP4)
button4.direction = digitalio.Direction.INPUT
button4.pull = digitalio.Pull.UP

#current call button
button5 = digitalio.DigitalInOut(board.GP21)
button5.direction = digitalio.Direction.INPUT
button5.pull = digitalio.Pull.UP

button6 = digitalio.DigitalInOut(board.GP20)
button6.direction = digitalio.Direction.INPUT
button6.pull = digitalio.Pull.UP

MuteButton = digitalio.DigitalInOut(board.GP6)
MuteButton.direction = digitalio.Direction.INPUT
MuteButton.pull = digitalio.Pull.UP
muteState = False

# s0 = digitalio.DigitalInOut(board.GP16)
# s1 = digitalio.DigitalInOut(board.GP17)
# s2 = digitalio.DigitalInOut(board.GP18)
# s3 = digitalio.DigitalInOut(board.GP19)
# Sig = digitalio.DigitalInOut(board.GP28)
# controlPin = [s0, s1, s2, s3]

# muxChannel = [
#    {0,0,0,0}, 
#    {1,0,0,0}, 
#    {0,1,0,0}, 
#    {1,1,0,0}, 
#    {0,0,1,0}, 
#    {1,0,1,0}, 
#    {0,1,1,0}, 
#    {1,1,1,0}, 
#    {0,0,0,1}, 
#    {1,0,0,1}, 
#    {0,1,0,1}, 
#    {1,1,0,1}, 
#    {0,0,1,1}, 
#    {1,0,1,1}, 
#    {0,1,1,1}, 
#    {1,1,1,1}  
# ]

# Do we need to define direction and pull? 
#Insert Deafen

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(kbd)
cc = ConsumerControl(usb_hid.devices)

pot = analogio.AnalogIn(board.GP27)
last_position = 0

fakeVolume = 0

for x in range(100):
    cc.press(ConsumerControlCode.VOLUME_DECREMENT)

while True:
    #Upload button 
    if not button1.value:
        print('button three pressed')
        kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.U)
    # Code button (Top left)
    if not button2.value:
        button6Count = 0
        print("Button 6 has just been pressed")
        while button6Count < 6:
            kbd.send(Keycode.GRAVE_ACCENT)
            button6Count = button6Count + 1
            if button6Count == 3:
                kbd.send(Keycode.ENTER)
                kbd.send(Keycode.ENTER)

            if button6Count == 6:
                kbd.send(Keycode.UP_ARROW)
                keyboard_layout.write("ENTER CODE IN HERE")
                kbd.send(Keycode.DOWN_ARROW)
                kbd.send(Keycode.ENTER)
     #Unread channels button           
    if not button3.value:
        kbd.send(Keycode.OPTION, Keycode.SHIFT, Keycode.DOWN_ARROW)
    
    if not button4.value:
        kbd.send(Keycode.COMMAND, Keycode.P)
    #navigate to current call 
    if not button5.value: 
        print("Hello world")
        kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.OPTION, Keycode.V)
    #Unread messages button
    if not button6.value:
        kbd.send(Keycode.COMMAND, Keycode.I)
        
    #MUTE
    if not MuteButton.value:
        print(MuteButton.value)
        if muteState:
            kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.M)
            kbd.release(Keycode.COMMAND, Keycode.SHIFT, Keycode.M)
            muteState = False
            time.sleep(1)
    else:
        if not muteState:
            kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.M)
            kbd.release(Keycode.COMMAND, Keycode.SHIFT, Keycode.M)
            muteState = True
            time.sleep(1)
            
    potVal = round((pot.value / 65536) * 50)

    if (potVal % 2) == 0:
        print ("The provided number is even")

    else:
        print ("The provided number is odd")
        potVal = potVal - 1


    print("PotVal: " ,potVal)
    print("FakeVolume: " ,fakeVolume)


    if potVal > fakeVolume:
        if not fakeVolume == 100 :
            fakeVolume = fakeVolume+2
            cc.press(ConsumerControlCode.VOLUME_INCREMENT)
            # cc.release()

    if potVal < fakeVolume:
        if not fakeVolume == 0 :
            fakeVolume = fakeVolume-2
            cc.press(ConsumerControlCode.VOLUME_DECREMENT)
            # cc.release()
          
    time.sleep(0.3)
    kbd.release_all()   
    cc.release()
