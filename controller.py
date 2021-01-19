from tkinter import *
from tkinter import ttk
import serial.tools.list_ports

class DelayChannel:
    def __init__(self, channel, index, base_row, base_col):
        self.channel = channel
        self.index = index

        module = index+3 if channel == 'l' else index+8
        self.scale_vol = Scale(master=root, from_=4, to=0, resolution = 0.01, command=handleVolume(module, 0, self), length = 200, label = 'vol', troughcolor='green')
        self.scale_vol.grid(row = base_row, column = base_col, padx=0, pady=5)
        self.scale_vol.set(0)

        register = index+2 if channel == 'l' else index+7
        self.scale_del = Scale(master=root, from_=6, to=0, resolution = 0.01, command=handleDelay(1, register, self), length = 200, label = 'del')
        self.scale_del.grid(row = base_row, column = base_col+1, padx=0, pady=5)
        self.scale_del.set(0)

        self.label = Label(master=root, text=self.getName())
        self.label.grid(row = base_row+1, column = base_col, padx=0, pady=5)

        self.enable = BooleanVar()
        self.checkbox = Checkbutton(master=root, text='enable', var=self.enable, command=updateCheckbox)
        self.checkbox.grid(row = base_row+1, column = base_col+1, padx=0, pady=5)
        if channel == 'l':
            checkboxes_left.append(self.enable)
        else:
            checkboxes_right.append(self.enable)

    def getName(self):
        return self.channel + str(self.index)

def sendVal(module, register, value):
    send = 'M' + str(module) + 'R' + str(register) + '=' + str(int(value))
    if ser.is_open:
        ser.write((send + '\r\n').encode('ascii'))
    print(send)

def sendVolume(module, register, slider):
    val = slider.get() * 64
    if val > 255:
        val = 255
    sendVal(module, register, val)

def sendDelay(module, register, slider):
    val = slider.get() * 43
    if val > 255:
        val = 255
    sendVal(module, register, val)

def handleSlider(i):
    module = 2 if i == 0 else 13
    return lambda val : sendVolume(module, 0, faders[i])

def handleVolume(module, register, slider):
    return lambda val : sendVolume(module, register, slider.scale_vol)

def handleDelay(module, register, slider):
    return lambda val : sendDelay(module, register, slider.scale_del)

def updateCheckbox():
    val = 0
    for count, box in enumerate(checkboxes_left):
        val |= box.get() << count
    sendVal(1, 0, val)
    val = 0
    for count, box in enumerate(checkboxes_right):
        val |= box.get() << count
    sendVal(1, 1, val)

def openSerial():
    if ser.is_open:
        print('Closing port: ', ser.port)
        ser.close()
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.stopbits = serial.STOPBITS_ONE
    ser.parity = serial.PARITY_NONE
    ser.port = combo.get()
    print('Connect to:', ser.port)
    ser.open()

root = Tk()
root.title('Register Interface')

ser = serial.Serial()

# enable-boxes
checkboxes_left = []
checkboxes_right = []

# volume faders
faders = []
fadernames = ['vol_l', 'vol_r']
for i in range(2):
    faders.append(Scale(master=root, from_=4, to=0, resolution = 0.01, command=handleSlider(i), length = 200, label = fadernames[i], troughcolor='blue'))
    faders[i].grid(row = i*2, column = 1, padx=0, pady=5)
    faders[i].set(1)
    enable = BooleanVar()
    checkbox = Checkbutton(master=root, text='enable_del', var=enable, command=updateCheckbox)
    checkbox.grid(row = i*2+1, column = 1, padx=0, pady=5)
    if fadernames[i] == 'vol_l':
        checkboxes_left.append(enable)
    else:
        checkboxes_right.append(enable)

# delay controls
delays = []
for i in range(7):
    delays.append(DelayChannel('l', i, 0, i*2+3))
    delays.append(DelayChannel('r', i, 2, i*2+3))

# port selection combobox
ports = [port.device for port in serial.tools.list_ports.comports()]
combo = ttk.Combobox(root, values=ports)
combo.grid(row=0, column=0)

# connect button
connButton = Button(root, text="Connect", command=openSerial)
connButton.grid(row=1, column=0)

root.mainloop()
