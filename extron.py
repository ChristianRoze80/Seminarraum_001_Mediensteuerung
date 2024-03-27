class Projektor:
    def __init__(self):
        self.port = None
        self.baud = None
        self.timeout = None
        self.xonxoff = None
        self.status = None
        self.input = None
        self.schnittstelle = None
    def set(self,command):                            #Funktion zum senden des passenden RS232 Kommandos
        ValueSetValues = {   'on'    : '0B',
                             'off'   : '2B',
                             'input1': '1!',
                             'input2': '2!',
                             'input3': '3!',
                             'input4': '4!'
                             }
        if __debug__:
            print('Befehl --> Projektor:' + command)
        self.schnittstelle.flush()                                      #Empfangspuffer leeren
        self.schnittstelle.write(ValueSetValues[command].encode())      #Kommando senden
        if command == 'on':                                             #Wenn Kommando 'on' ...
            self.get_feedback('pwr_status')                             #Feedback empfangen
        elif command == 'off':                                          #... oder 'off' ist
            self.get_feedback('pwr_status')                             #Feedback empfangen
        else:
            self.get_feedback('input_status')                           #Feedback empfangen

    def get(self,command):                  #Funktion um den Status abzufragen
        ValueGetValues = {  'pwr_status'    : b'B',
                            'input_status'  : b'!'
                            }
        if __debug__:
            print('Befehl --> Projektor:' + command)
        self.schnittstelle.flush()
        self.schnittstelle.write(ValueGetValues[command])

        if command == 'pwr_status':         #"0" or "2"
            temp = self.schnittstelle.read(3)
            if len(temp) == 3:
                self.status = temp[0] - 48
            else:
               self.status = 'unknown'
            if __debug__:
                print('Antwort <-- Projektor:Status:' + str(self.status))

        if command == 'input_status':       #"1" oder "2" oder "3" oder "4"
            temp = self.schnittstelle.read(3)
            if len(temp) == 3:
                self.input = temp[0] - 48
            else:
               self.input = 'unknown'
            if __debug__:
                print('Antwort <-- Projektor:Input:'+ str(self.input))

    def get_feedback(self,command): #Funktion um das Feedback nach dem Senden von Befehle zu empfangen
        if command == 'pwr_status':             #Soll der Power Status abgefragt werden ?
            temp = self.schnittstelle.read(6)   #6 Bytes empfangen (Gerät sendet als Status  'Vmt0'+CR+LF
            if len(temp) == 6:                  #Wenn 6 Bytes empfangen wurden
                self.status = temp[3] - 48      #4. Byte auslesen und in Integer umwandeln
            else:                               #Wenn innerhalb Timeout keine 6 Bytes empfangen wurden
               self.status = 'unknown'          #Status auf 'unknown' setzen
            if __debug__:
                print('Antwort <-- Projektor:Status:' + str(self.status))

        if command == 'input_status':           #Soll der Input Status abgefragt werden ?
            temp = self.schnittstelle.read(9)  # 9 Bytes empfangen (Gerät sendet als Antwort auf vorherigen Befehl 9 Bytes ('InX All'+CR+LF)
            if len(temp) == 9:
                self.input = temp[2] - 48       # 3. Byte auslesen und in Integer umwandeln
            else:
               self.input = 'unknown'           #Wenn keine 9 Bytes innerhalb der Timeoutzeit empfangen wurden Input Status auf 'unknown' setzen
            if __debug__:
                print('Anwort <-- Projektor:Input:'+ str(self.input))

