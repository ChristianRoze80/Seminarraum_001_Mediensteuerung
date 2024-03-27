import serial
class Kamera():
    def __init__(self):
        self.port = None
        self.baud = None
        self.timeout = None
        self.xonxoff = None
        self.schnittstelle = None
        self.movecmd = b'\x81\x01\x06\x01\x01\x01'
        self.zoomcmd = b'\x81\x01\x04\x07'
        self.presetcmd = b'\x81\x01\x04\x3F\x02'
    def move(self,direction):       #Funktion um Befehle zum Bewegen der Kamera zu senden
        ValueMoveValues= {'left':   b'\x01\x03\xFF',
                          'right':  b'\x02\x03\xFF',
                          'up':     b'\x03\x01\xFF',
                          'down':   b'\x03\x02\xFF',
                          'stop':   b'\x03\x03\xFF'
        }
        print(self.movecmd + ValueMoveValues[direction])
        serial.Serial(self.port, self.baud, xonxoff=self.xonxoff, timeout=self.timeout).write(self.movecmd + ValueMoveValues[direction])
    def zoom(self,direction):       #Funktion um Befehle zum Zoomen der Kamera zu senden
        ValueZoomValues= {'+':      b'\x02\xFF',
                          '-':      b'\x03\xFF',
                          'stop':   b'\x00\xFF'
                          }
        print(self.zoomcmd + ValueZoomValues[direction])
        serial.Serial(self.port, self.baud, xonxoff=self.xonxoff, timeout=self.timeout).write(self.zoomcmd + ValueZoomValues[direction])

    def preset(self,number):    #Funktion um Befehle zum aufrufen der Presets zu senden
        ValuePresetValues = {'0': b'\x00\xFF',
                             '1': b'\x01\xFF',
                             '2': b'\x02\xFF',
                             '3': b'\x03\xFF'
                           }
        print(self.presetcmd + ValuePresetValues[number])
        serial.Serial(self.port, self.baud, xonxoff=self.xonxoff, timeout=self.timeout).write(self.presetcmd + ValuePresetValues[number])










