class Stream:
    def __init__(self):
        self.port = None
        self.baud = None
        self.timeout = None
        self.xonxoff = None
        self.input = None
        self.schnittstelle = None
    def set(self,command):  #Funktion zum senden des passenden RS232 Kommandos mit anschließender auswertung des Feedbacks
        ValueSetValues = {   'input1': b'\x02PGM:0;',
                             'input2': b'\x02PGM:1;',
                             'input3': b'\x02PGM:2;',
                             'input4': b'\x02PGM:3;'
                             }
        if self.input != int(command[5]):   #Nur ausführen wenn Gerät noch nicht auf dem gewünschten Eingang steht
            self.schnittstelle.flush()      #Empfangspuffer leeren
            self.schnittstelle.write(ValueSetValues[command])   #Kommando senden
            temp = self.schnittstelle.read(8)   #8 Bytes Empfangen (Gerät sendet 1Byte "ACK" als Antwort und dann 7Byte "STX"QPG:a; (a ist der gewählte Eingang von 0 beginnen)
            if len(temp) == 8:                  #Wenn 8 Bytes Empfangen wurden
                self.input = temp[6] - 48 + 1   # 7. Byte auslesen, in Integer umwandel und da Eingang am Gerät mit 0 beginnt 1 dazu addieren
            else:                               #Wenn keine 8 Bytes innerhalb der Timeout Zeit empfangen wurden
                self.input = 'unknown'          #Input auf 'unknown' setzen
            if __debug__:
                print('Anwort <-- Stream:Input:' + str(self.input))

        else:
            if __debug__:
                print('Gleich:    ' + str(self.input) + ' != ' + str(command[5]))

    def get(self,command):  #Funktion zum abfragen des Eingangs-Status
        ValueGetValues = {  'input_status'  : b'\x02QPG;'}
        if __debug__:
            print('Befehl --> Stream:' + command)
        self.schnittstelle.flush()          #Empfangspuffer leeren
        self.schnittstelle.write(ValueGetValues[command]) #Kommando senden

        temp = self.schnittstelle.read(7)   #7Bytes Empfangen (Gerät sendet als Antwort 7Byte "STX"QPG:a; (a ist der gewählte Eingang von 0 beginnen
        if len(temp) == 7:                  #Wenn 7 Bytes Empfangen wurden
            self.input = temp[5] - 48 + 1   # 5. Byte auslesen,in Integer umwandel und da Eingang am Gerät mit 0 beginnt 1 dazu addieren
        else:                               #Wenn keine 8 Bytes innerhalb der Timeout Zeit empfangen wurden
            self.input = 'unknown'          #Input auf 'unknown' setzen
        if __debug__:
            print('Anwort <-- Stream:Input:'+ str(self.input))