from tkinter import *
from tkinter import ttk
import serial.tools.list_ports

def sendVal(i):
    send = 'M' + str(i+1) + 'R0=' + str(int(faders[i].get() * 64))
    if ser.is_open:
        ser.write((send + '\r\n').encode('ascii'))
    print(send)

def handleSlider(i):
    return lambda val : sendVal(i)

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
fadernames = ['left', 'right']
for i in range(2):
    faders.append(Scale(master=root, from_=2, to=0, resolution = 0.025, command=handleSlider(i), length = 200, label = fadernames[i]))
    faders[i].grid(row = 0, column = i, padx=5, pady=5)
    faders[i].set(1)

# port selection combobox
ports = [port.device for port in serial.tools.list_ports.comports()]
combo = ttk.Combobox(root, values=ports)
combo.grid(row=1, column=0)

# connect button
connButton = Button(root, text="Connect", command=openSerial)
connButton.grid(row=1, column=1)

root.mainloop()
