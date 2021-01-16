from tkinter import *
from tkinter import ttk
import serial.tools.list_ports

class DelayChannel:
    def __init__(self, channel, index, base_row, base_col):
        self.channel = channel
        self.index = index
        self.enable = False
        self.scale_vol = Scale(master=root, from_=4, to=0, resolution = 0.01, command=handleVolume(index, 0, self), length = 200, label = 'vol', troughcolor='green')
        self.scale_vol.grid(row = base_row, column = base_col, padx=0, pady=5)
        self.scale_vol.set(0)
        self.scale_del = Scale(master=root, from_=6, to=0, resolution = 0.01, command=handleDelay(index, 0, self), length = 200, label = 'del')
        self.scale_del.grid(row = base_row, column = base_col+1, padx=0, pady=5)
        self.scale_del.set(0)
        self.label = Label(master=root, text=self.getName())
        self.label.grid(row = base_row+1, column = base_col, padx=0, pady=5)
        self.checkbox = Checkbutton(master=root, text='enable', var=self.enable)
        self.checkbox.grid(row = base_row+1, column = base_col+1, padx=0, pady=5)

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
    return lambda val : sendVolume(i, 0, faders[i])

def handleVolume(module, register, slider):
    return lambda val : sendVolume(module, register, slider.scale_vol)

def handleDelay(module, register, slider):
    return lambda val : sendDelay(module, register, slider.scale_del)

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

# faders
faders = []
fadernames = ['vol_l', 'vol_r']
for i in range(2):
    faders.append(Scale(master=root, from_=4, to=0, resolution = 0.01, command=handleSlider(i), length = 200, label = fadernames[i], troughcolor='blue'))
    faders[i].grid(row = i*2, column = 1, padx=0, pady=5)
    faders[i].set(1)

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
