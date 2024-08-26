#import sys
#sys.exit(0)


import serial
import time
import csv
import pandas as pd
from sense_hat import SenseHat
from datetime import datetime
import math
sense = SenseHat()
b = [255 , 255 , 255]

verde = [0 , 255 , 0]
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

ser = serial.Serial ( '/dev/Senzori', 9600 )
ser.baudrate = 9600

def dai_tati():
    line = ser.readline()
    
    words = line.split()
    try:
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        dist = (float)(words[2])
        co2 = (int)(words[5])
        nh3 = (int)(words[8])
        h2 = (int)(words[11])
        pressure = round(sense.get_pressure() , 5)
        temp = round(sense.get_temperature() , 5)
        compass = sense.get_compass_raw()
        #print("oki")
        
        mag = round( math.sqrt( compass["x"]*compass["x"] + compass["y"]*compass["y"] + compass["z"]*compass["z"]) , 6 )
        print(line, end = ' ')
        print(pressure, end = ' ')
        print(temp, end = ' ')
        print(mag)

    except:
        print("daca vezi asta ceva e foarte foarte rau")
        a = 1


def iscf ( ch ) :
    return ch >= '0' and ch <= '9'

i = 0
def getnum ( s ) :
    sz = len ( s )
    global i
    
    while i < sz and iscf ( s[i] ) == False :
        i += 1

    nr = 0
    while i < sz and iscf ( s[i] ) == True :
        nr = nr * 10 + int ( s[i] )
        i += 1

    p10 = 1
    if i < sz and s[i] == '.' :
        i += 1
        while i < sz and iscf ( s[i] ) == True :
            nr = nr * 10 + int ( s[i] )
            p10 *= 10
            i += 1

    if p10 == 1 :
        return nr
    else :
        return float ( nr / p10 )

if __name__ == '__main__':
    setup ={'Nh3' :['0'] , 'Co2': ['0'] ,'H2':['0'] , 'Distance' :['0'] , 'Pressure':['0'] , 'Temperature':['0'],'Compass':['0'] , 'Time':['0']}
    df = pd.read_csv('/home/pi/Desktop/senzori_pandas.csv')
    print(df)
    for i in range(1080):
        line = ser.readline()
    
        words = line.split()
        try:
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            dist = (float)(words[2])
            co2 = (int)(words[5])
            nh3 = (int)(words[8])
            h2 = (int)(words[11])
            pressure = round(sense.get_pressure() , 5)
            temp = round(sense.get_temperature() , 5)
            compass = sense.get_compass_raw()
            print("oki")
        
            mag = round( math.sqrt( compass["x"]*compass["x"] + compass["y"]*compass["y"] + compass["z"]*compass["z"]) , 6 )
            print(line ,end = ' ')
            print(pressure, end = ' ')
            print (temp , end = ' ')
            print (mag )

            df2 = pd.DataFrame({'Nh3': [nh3], 'Co2':[co2], 'H2':[h2] ,'Distance':[dist] , 'Pressure':[pressure] , 'Temperature':[temp] , 'Compass':[mag] , 'Time' : [current_time]} , columns = ['Nh3','Co2','H2','Distance','Pressure','Temperature','Compass','Time'])
            try:
                df = df.append(df2)
            except:
                print("prost")
            print(df2)
            df.to_csv("/home/pi/Desktop/senzori_pandas.csv", index = False)

        except:
            a = 1
        time.sleep(0.5)
    print(df)

