import socket
import json
import os
import sys
from _thread import*
import i2c_lcd
import time
import requests
from queue import Queue
lcd = i2c_lcd.lcd()
q = Queue(maxsize = 3)
f = open(os.devnull, 'w')
sys.stderr = f

def dedicated():
    while 1:
        while q.empty():
            lcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
            lcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 2)
        data = q.get()
        newdata = data.split(",")
        sum_len=len(newdata[0])
        lcd.lcd_clear()
        if newdata[3] == "High":
            for i in range(0,10):
                lcd.backlight_on(False)
                time.sleep(0.1)
                lcd.lcd_clear()
                time.sleep(0.1)
        if sum_len > 16:
            str_pad = " " * 16
            my_long_string = newdata[0]
            for i in range (0, len(my_long_string)):
                lcd.lcd_display_string(newdata[1], 2)
                lcd_text = my_long_string[i:(i+16)]
                lcd.lcd_display_string(lcd_text,1)
                time.sleep(0.2)
                if i == (sum_len-16):
                    break
                lcd.lcd_display_string(str_pad,1)
        else:
            lcd.lcd_display_string(newdata[0],1)
            lcd.lcd_display_string(newdata[1],2)
        time.sleep(int(newdata[2]))
        lcd.lcd_clear()

def display_string(message):
    try:
        data = json.loads(message.decode('utf-8'))
        first = data["1"]
        second = data["2"]
        time_sec = data["time"]
        priority = data["priority"]
        newstr=str(first)+','+str(second)+','+str(time_sec)+','+str(priority)
        q.put(newstr)
    except EOFError as error:
        pass

def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        display_string(data)
    connection.close()

def run_server():
    ServerSocket = socket.socket()
    host = '127.0.0.1'
    port = 1233
    ThreadCount = 0
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    ServerSocket.listen(5)
    start_new_thread(dedicated, ())
    while True:
        Client, address = ServerSocket.accept()
        start_new_thread(threaded_client, (Client, ))
    ServerSocket.close()
        
if __name__ == "__main__":
    run_server()
