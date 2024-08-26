# from wireless import Wireless
# wireless = Wireless() 
# wireless.connect(ssid='ssid', password='password') 

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import serial
from sense_hat import SenseHat

ser = serial.Serial('/dev/motoare', 9600 , timeout = 1)
ser1 = serial.Serial('/dev/Senzori' , 9600 , timeout =1)
#ser1 = serial.Serial('/dev/ttyUSB0' , 9600 , timeout =1)

sense = SenseHat()
b = [255 , 255 , 255]

v = [0 , 255 , 0]
r = [255 , 0 , 0]
def afisare_senseHat(verde):
    afiseaza = [
        verde , verde , verde, verde , verde , verde , verde , verde ,
        verde , verde , verde, verde , verde , verde , verde , verde ,
        verde , verde , verde, verde , verde , verde , verde , verde ,
        verde , verde , verde, verde , verde , verde , verde , verde ,
        verde , verde , verde, verde , verde , verde , verde , verde ,
        verde , verde , verde, verde , verde , verde , verde , verde ,
        verde , verde , verde, verde , verde , verde , verde , verde ,
        verde , verde , verde, verde , verde , verde , verde , verde 
    ]
    sense.set_pixels(afiseaza)

def bimbimbambam():
    bum = [[255 - (idx // 8 + idx % 8) * 16, 0, (idx // 8 + idx % 8) * 16] for idx in range(64)]
    sense.set_pixels(bum)

bimbimbambam()

class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin','*')

        self.end_headers()

    def do_GET(self):
        global sense

        if str(self.path) == "/move/centru":
            ser.write("Centru\n".encode('utf-8'))
            print("Centru")
        if str(self.path) == "/move/stop":
            ser.write("Stop\n".encode('utf-8'))
            print("Stop")
        if str(self.path) == "/move/fata":
            ser.write("Fata\n".encode('utf-8'))
            print("Fata")
        if str(self.path) == "/move/spate":
            ser.write("Spate\n".encode('utf-8'))
            print("Spate")
        if str(self.path) == "/move/stanga": 
            ser.write("Stanga\n".encode('utf-8'))
            print("Stanga")
        if str(self.path) == "/move/dreapta": 
            ser.write("Dreapta\n".encode('utf-8'))
            print("Dreapta")

        if str(self.path) == "/move/fatatesla":
            ser.write("FataTesla\n".encode('utf-8'))
            print("FataTesla")

        if str(self.path) == "/move/spatetesla":
            ser.write("SpateTesla\n".encode('utf-8'))
            print("SpateTesla")            

        if str(self.path) == "/gheara/open": 
            ser1.write("Open\n".encode('utf-8'))
            print("Open")
        
        if str(self.path) == "/gheara/close": 
            ser1.write("Close\n".encode('utf-8'))
            print("Close")
        if str(self.path) == "/move/dealfata": 
            ser.write("UDF\n".encode('utf-8'))
            print("UDF")
        if str(self.path) == "/move/dealspate": 
            ser.write("UDS\n".encode('utf-8'))
            print("UDS")

        # dau cu str() ca am eu paranoia
        line = str(ser1.readline().decode("utf-8"))
        pressure = round(sense.get_pressure(), 5)
        temp = round(sense.get_temperature(), 5)
        #compass = sense.get_compass_raw()
        #print("oki")
        
        #mag = round( math.sqrt( compass["x"]*compass["x"] + compass["y"]*compass["y"] + compass["z"]*compass["z"]) , 6 )
        #print(line, end = ' ')
        #print(pressure, end = ' ')
        #print(temp, end = ' ')
        #print(mag)

        #print(line)
        #words = line.split()
        #distance = (float)(words[2])
        #mq135 = (int)(words[5])
        #mq8 = (int)(words[8])

        line += " temperature = {} pressure = {} \n".format(temp, pressure)
        
        self._set_response()
        self.wfile.write(("GET request for {} | " + str(line)).format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8080):


    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        #afisare_senseHat([0, 0, 255]) # doamne ajuta cu albastrul ala
        bimbimbambam()
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
	# nu se ajunge aici de obicei
        run()
        #afisare_senseHat([0, 0, 255])
