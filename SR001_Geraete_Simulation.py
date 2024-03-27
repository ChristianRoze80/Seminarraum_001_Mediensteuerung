# Dieses Programm steuert die Medientechnik im Seminarraum 0.01 bestehend aus
# COM4 Extron #Videoscaler Typ IN1604 DTP
# COM5 Roland Streaming gerät Typ VR-4HD
# COM6 Marshal Kamera Typ CV610-U3 (Whiteboard Kamera)
# COM7 Marshal Kamera Typ CV610-U3 (Tafel Kamera)
# die GUI ist mit TKINTER realisiert, für die Feedbacks der Buttons werden die echten Antworten der
# entsprechenden Geräte verwendet

import sys
import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *

from extron import *
from roland import *
from mar import Kamera
import serial


def resource(relative_path):  # Diese Funktion wird zum Verwenden des ICONS in pyinstaller benötigt
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
image = resource("Universität_Heidelberg.ico")


def check_port_status(port_name: str):  # Diese Funktion überprüft ob die Schnittstelle vorhanden und frei ist
    if port_name is None:
        return
    try:
        serial_port = serial.Serial(port=port_name, baudrate=9600, timeout=0.1)
        read_data = serial_port.read()
    except serial.SerialException as err:
        print("Can not open serial port " + port_name)
        print('Exception Details --> ', err)
        return(False)
    else:
        print("serial port " + port_name + " is available and not in use")
        serial_port.close()
        return (True, 1)

# Hauptfenster
window = tk.Tk()
window.attributes("-topmost", True)
window.title('ACI Seminarraum 0.01 Mediensteuerung')
window.geometry('444x360')
window.iconbitmap(image)
window.resizable(width=False, height=False)
style = ttk.Style("cosmo")
style.configure('TButton', font=('Arial', 8))
style.map('TButton')



# Frame Projektor Bedienung
projektor = ttk.LabelFrame(window, text='Projektor', bootstyle="PRIMARY")
projektor.place(x=5, y=5, width=434, height=90)
# //Frame Projektor Bedienung

# Frame Streaming
videokonferenz = ttk.LabelFrame(window, text='Videokonferenz', bootstyle="warning")
videokonferenz.place(x=5, y=105, width=434, height=90)
videokonferenz.columnconfigure(0, minsize=90)
# //Frame Streaming

# Die folgenden beiden Frames liegen genau übereinander (Kamera1 unten, Kamera2 darüber)
# je nachdem welche Kamera ausgewählt wird, wird der Frame Kamera2 aus und eingeblendet

# Frame Kamera1 Steuerung
kamera1 = ttk.LabelFrame(window, text='Kamera Steuerung', bootstyle="danger")
kamera1.place(x=5, y=205, width=434, height=150)
cam = tk.Variable(kamera1, 2)
kamera_control1 = ttk.Frame(kamera1)
kamera_control1.place(x=5, y=40, height=85)
kamera_presets1 = ttk.LabelFrame(kamera1, text='Voreingestellte Positionen')
kamera_presets1.place(x=190, y=5, height=50)
# //Frame Kamera1 Steuerung

# Frame Kamera2 Steuerung
kamera2 = ttk.LabelFrame(window, text='Kamera Steuerung', bootstyle="danger")
kamera2.place(x=5, y=205, width=434, height=150)
kamera_control2 = ttk.Frame(kamera2)
kamera_control2.place(x=5, y=40, height=85)
kamera_presets2 = ttk.LabelFrame(kamera2, text='Voreingestellte Positionen')
kamera_presets2.place(x=190, y=5, height=50)
# //Frame Kamera2 Steuerung



# Erzeugen der Objekte
# Kamera Whiteboard
cam1 = Kamera()
cam1.port = 'COM6'
cam1.baud = 9600
cam1.timeout = 1
cam1.xonxoff = False
if not check_port_status(port_name=cam1.port):
    mb =Messagebox.show_warning('Fehler beim öffnen der Seriellen Schnittstelle: ' + cam1.port)
    sys.exit()  # Schließen des Fensters
#cam1.schnittstelle = serial.Serial(port=cam1.port, baudrate=cam1.baud, xonxoff=cam1.xonxoff,
#                                         timeout=cam1.timeout)

# Kamera Tafel
cam2 = Kamera()
cam2.port = 'COM7'
cam2.baud = 9600
cam2.timeout = 1
cam2.xonxoff = False
if not check_port_status(port_name=cam2.port):
    mb =Messagebox.show_warning('Fehler beim öffnen der Seriellen Schnittstelle: ' + cam2.port)
    sys.exit()  # Schließen des Fensters
#cam2.schnittstelle = serial.Serial(port=cam2.port, baudrate=cam2.baud, xonxoff=cam2.xonxoff,
#                                        timeout=cam2.timeout)

# #Extron Scaler
projektor1 = Projektor()
projektor1.port = 'COM4'
projektor1.baud = 9600
projektor1.timeout = 0.5
projektor1.xonxoff = False
if not check_port_status(port_name=projektor1.port):
    mb =Messagebox.show_warning('Fehler beim öffnen der Seriellen Schnittstelle: ' + projektor1.port)
    sys.exit()  # Schließen des Fensters
projektor1.schnittstelle = serial.Serial(port=projektor1.port, baudrate=projektor1.baud, xonxoff=projektor1.xonxoff,
                                         timeout=projektor1.timeout)



# Roland Streaming Device
stream1 = Stream()
stream1.port = 'COM5'
stream1.baud = 9600
stream1.timeout = 0.5
stream1.xonxoff = True
if not check_port_status(port_name=stream1.port):
    mb =Messagebox.show_warning('Fehler beim öffnen der Seriellen Schnittstelle: ' + stream1.port)
    sys.exit()  # Schließen des Fensters
stream1.schnittstelle = serial.Serial(port=stream1.port, baudrate=stream1.baud, xonxoff=stream1.xonxoff,
                                      timeout=stream1.timeout)

# Funktionen, ob die Buttes gedrückt oder losgelassen werden
# Kamera1
def move_up1(self):
    print('UP')
    cam1.move('up')


def move_down1(self):
    print('DOWN')
    cam1.move('down')


def move_left1(self):
    print('LEFT')
    cam1.move('left')


def move_right1(self):
    print('RIGHT')
    cam1.move('right')


def zoom_in1(self):
    print('ZOOM +')
    cam1.zoom('+')


def zoom_out1(self):
    print('ZOOM -')
    cam1.zoom('-')


def move_stop1(self):
    print('MOVE STOP')
    cam1.move('stop')


def zoom_stop1(self):
    print('ZOOM STOP')
    cam1.zoom('stop')


def preset_11():
    print('Preset 1')
    cam1.preset('0')


def preset_21():
    print('Preset 2')
    cam1.preset('1')


def preset_31():
    print('Preset 3')
    cam1.preset('2')


def preset_41():
    print('Preset 4')
    cam1.preset('3')
# //Kamera1

# Kamera2


def move_up2(self):
    print('UP')
    cam2.move('up')


def move_down2(self):
    print('DOWN')
    cam2.move('down')


def move_left2(self):
    print('LEFT')
    cam2.move('left')


def move_right2(self):
    print('RIGHT')
    cam2.move('right')


def zoom_in2(self):
    print('ZOOM +')
    cam2.zoom('+')


def zoom_out2(self):
    print('ZOOM -')
    cam2.zoom('-')


def move_stop2(self):
    print('MOVE STOP')
    cam2.move('stop')


def zoom_stop2(self):
    print('ZOOM STOP')
    cam2.zoom('stop')


def preset_12():
    print('Preset 1')
    cam2.preset('0')


def preset_22():
    print('Preset 2')
    cam2.preset('1')


def preset_32():
    print('Preset 3')
    cam2.preset('2')


def preset_42():
    print('Preset 4')
    cam2.preset('3')
# //Kamera2

# Funktion zum Aktualisieren der Button Feedbacks


def update_stat():
    # #Extron
    if projektor1.status == 0:
        ein.state(["selected"])
    else:
        ein.state(["!selected"])

    if projektor1.status == 2:
        aus.state(["selected"])
    else:
        aus.state(["!selected"])

    if projektor1.input == 3:
        fpc.state(["selected"])
    else:
        fpc.state(["!selected"])

    if projektor1.input == 2:
        hdmi_beamer.state(["selected"])
    else:
        hdmi_beamer.state(["!selected"])

    if projektor1.input == 1:
        vga_beamer.state(["selected"])
    else:
        vga_beamer.state(["!selected"])

    if projektor1.input == 4:
        dcam_beamer.state(["selected"])
    else:
        dcam_beamer.state(["!selected"])
    # //#Extron

    # Roland
    if stream1.input == 1:
        stream_1.state(["selected"])
    else:
        stream_1.state(["!selected"])

    if stream1.input == 3:
        stream_2.state(["selected"])
    else:
        stream_2.state(["!selected"])

    if stream1.input == 4:
        stream_3.state(["selected"])
    else:
        stream_3.state(["!selected"])

    if stream1.input == 2:
        stream_4.state(["selected"])
    else:
        stream_4.state(["!selected"])
    # //Roland

# Funktionen um die Funktionen innerhalb der Module aufrufen zu können (geht nicht direkt Button --> Modul Funktion)


def prj(command):
    projektor1.set(command)
    update_stat()

def einschaltsequenz():
    ein.state(['disabled'])
    projektor1.set('input3')
    projektor1.set('on')
    update_stat()
    window.update()
    projektor1.set('off')
    projektor1.set('on')
    projektor1.set('off')
    projektor1.set('on')
    projektor1.set('off')
    projektor1.set('on')
    ein.state(['!disabled'])


def stream(command):
    stream1.set(command)
    update_stat()


# Platzieren der Knöpfe und RadioButtons
# Projektor
ein = ttk.Button(projektor, text="Ein", command=lambda: einschaltsequenz(), bootstyle="toolbutton")
ein.grid(column=0, row=0, padx=2, pady=2, sticky=tk.E+tk.W)

aus = ttk.Button(projektor, text="Aus", command=lambda: prj('off'), bootstyle="toolbutton")
aus.grid(column=0, row=1, padx=2, pady=2)

fpc = ttk.Button(projektor, text="Fest PC Pult", command=lambda: prj('input3'), bootstyle="toolbutton")
fpc.grid(column=1, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S)

hdmi_beamer = ttk.Button(projektor, text="HDMI Pult \n\"Laptop\nBeamer\"", command=lambda: prj('input2'),
                         bootstyle="toolbutton")
hdmi_beamer.grid(column=2, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S)

vga_beamer = ttk.Button(projektor, text="VGA Pult", command=lambda: prj('input1'), bootstyle="toolbutton")
vga_beamer.grid(column=3, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S)

dcam_beamer = ttk.Button(projektor, text="Dokumenten\nKamera", command=lambda: prj('input4'), bootstyle="toolbutton")
dcam_beamer.grid(column=4, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S)

# Streaming
stream_1 = ttk.Button(videokonferenz, text="HDMI Pult\n\"Laptop\nStreaming\"", command=lambda: stream('input1'),
                      bootstyle="warning-toolbutton")
stream_1.grid(column=1, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

stream_2 = ttk.Button(videokonferenz, text="Whiteboard\nKamera", command=lambda: stream('input3'),
                      bootstyle="warning-toolbutton")
stream_2.grid(column=2, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

stream_3 = ttk.Button(videokonferenz, text="Tafel\nKamera", command=lambda: stream('input4'),
                      bootstyle="warning-toolbutton")
stream_3.grid(column=3, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

stream_4 = ttk.Button(videokonferenz, text="Dokumenten\nKamera", command=lambda: stream('input2'),
                      bootstyle="warning-toolbutton")
stream_4.grid(column=4, row=0, padx=2, pady=2, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

# Kamera 1
WB_CAM = ttk.Radiobutton(kamera1, text="Whiteboard\nKamera", variable=cam, value=1)
WB_CAM.place(x=5, y=0, width=85, height=30)
BB_CAM = ttk.Radiobutton(kamera1, text="Tafel\nKamera", variable=cam, value=2,
                         command=lambda: kamera2.place(x=5, y=205, width=434, height=150))
BB_CAM.place(x=100, y=0, width=85, height=30)
UP = ttk.Button(kamera_control1, text="▲", bootstyle="light.solid")
UP.bind('<Button-1>', move_up1)
UP.bind('<ButtonRelease-1>', move_stop1)
UP.grid(column=1, row=0, sticky=tk.S)
DOWN = ttk.Button(kamera_control1, text="▼", bootstyle="light-solid")
DOWN.bind('<Button-1>', move_down1)
DOWN.bind('<ButtonRelease-1>', move_stop1)
DOWN.grid(column=1, row=2, sticky=tk.N)
LEFT = ttk.Button(kamera_control1, text="◄", bootstyle="light-solid")
LEFT.bind('<Button-1>', move_left1)
LEFT.bind('<ButtonRelease-1>', move_stop1)
LEFT.grid(column=0, row=1, sticky=tk.E)
RIGHT = ttk.Button(kamera_control1, text="►", bootstyle="light-solid")
RIGHT.bind('<Button-1>', move_right1)
RIGHT.bind('<ButtonRelease-1>', move_stop1)
RIGHT.grid(column=2, row=1, sticky=tk.W)
ZIN = ttk.Button(kamera_control1, text="+", bootstyle="light-solid")
ZIN.bind('<Button-1>', zoom_in1)
ZIN.bind('<ButtonRelease-1>', zoom_stop1)
ZIN.grid(column=4, row=0, sticky=tk.S)
ZOUT = ttk.Button(kamera_control1, text="-", bootstyle="light-solid")
ZOUT.bind('<Button-1>', zoom_out1)
ZOUT.bind('<ButtonRelease-1>', zoom_stop1)
ZOUT.grid(column=4, row=2, sticky=tk.N)
P1 = ttk.Button(kamera_presets1, text="Totale", command=preset_11, bootstyle="light-solid")
P1.grid(column=0, row=0, padx=2, pady=2)
P2 = ttk.Button(kamera_presets1, text="Links", command=preset_21, bootstyle="light-solid")
P2.grid(column=1, row=0, padx=2, pady=2)
P3 = ttk.Button(kamera_presets1, text="Rechts", command=preset_31, bootstyle="light-solid")
P3.grid(column=2, row=0, padx=2, pady=2)
# //Kamera 1

# Kamera 2
WB_CAM = ttk.Radiobutton(kamera2, text="Whiteboard\nKamera", variable=cam, value=1,
                         command=lambda: kamera2.place_forget())
WB_CAM.place(x=5, y=0, width=85, height=30)
BB_CAM = ttk.Radiobutton(kamera2, text="Tafel\nKamera", variable=cam, value=2)
BB_CAM.place(x=100, y=0, width=85, height=30)
UP = ttk.Button(kamera_control2, text="▲", bootstyle="light.solid")
UP.bind('<Button-1>', move_up2)
UP.bind('<ButtonRelease-1>', move_stop2)
UP.grid(column=1, row=0, sticky=tk.S)
DOWN = ttk.Button(kamera_control2, text="▼", bootstyle="light-solid")
DOWN.bind('<Button-1>', move_down2)
DOWN.bind('<ButtonRelease-1>', move_stop2)
DOWN.grid(column=1, row=2, sticky=tk.N)
LEFT = ttk.Button(kamera_control2, text="◄", bootstyle="light-solid")
LEFT.bind('<Button-1>', move_left2)
LEFT.bind('<ButtonRelease-1>', move_stop2)
LEFT.grid(column=0, row=1, sticky=tk.E)
RIGHT = ttk.Button(kamera_control2, text="►", bootstyle="light-solid")
RIGHT.bind('<Button-1>', move_right2)
RIGHT.bind('<ButtonRelease-1>', move_stop2)
RIGHT.grid(column=2, row=1, sticky=tk.W)
ZIN = ttk.Button(kamera_control2, text="+", bootstyle="light-solid")
ZIN.bind('<Button-1>', zoom_in2)
ZIN.bind('<ButtonRelease-1>', zoom_stop2)
ZIN.grid(column=4, row=0, sticky=tk.S)
ZOUT = ttk.Button(kamera_control2, text="-", bootstyle="light-solid")
ZOUT.bind('<Button-1>', zoom_out2)
ZOUT.bind('<ButtonRelease-1>', zoom_stop2)
ZOUT.grid(column=4, row=2, sticky=tk.N)
P1 = ttk.Button(kamera_presets2, text="Totale", command=preset_12, bootstyle="light-solid")
P1.grid(column=0, row=0, padx=2, pady=2)
P2 = ttk.Button(kamera_presets2, text="Links", command=preset_22, bootstyle="light-solid")
P2.grid(column=1, row=0, padx=2, pady=2)
P3 = ttk.Button(kamera_presets2, text="Rechts", command=preset_32, bootstyle="light-solid")
P3.grid(column=2, row=0, padx=2, pady=2)
P4 = ttk.Button(kamera_presets2, text="Pult", command=preset_42, bootstyle="light-solid")
P4.grid(column=3, row=0, padx=2, pady=2)
# //Kamera 2

# Initiale Statusabfrage beim Programmstart
projektor1.get('pwr_status')
projektor1.get('input_status')
stream1.get('input_status')
update_stat()

window.mainloop()       # Endlosschleife
sys.exit()              # Schließen des Fensters
