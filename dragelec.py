# !/usr/bin/env python
import raspitemp  # Raspberry CPU Temp reader
import readsensors  # reads wireless sensors
import decodexml  # reads & decodes the currentcost xml string
import datetime, time
import serial
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from random import randint
import pdb
import csv

# (aABTEMP,aACTEMP,aADTEMP,aAETEMP,aAZLIGHT,aABBATT,aACBATT,aADBATT,aAEBATT,aAZBATT)
# AE - Bedroom, AB - Front room,AD - Kitchen,AC - External,AZ - Light level

#SensorValues = (0,0,0,0,0,0,0,0,0,0)

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

def background_thread():
    alerttime = 300
    HighWatts = 5000
    LowWatts = 2000
    watts = TotalWatts = HiDuration = HighStart = AvgWatts = cost = RTemp = 0
    global ser
    global SensorValues
    while True:
        n = ser.inWaiting()
        if n != 0:
            USBTemps = ser.read(n)
            # print(USBTemps)
            SensorValues = readsensors.valueCheck(
                USBTemps,
                SensorValues[0],
                SensorValues[1],
                SensorValues[2],
                SensorValues[3],
                SensorValues[4],
                SensorValues[5],
                SensorValues[6],
                SensorValues[7],
                SensorValues[8],
                SensorValues[9])
        else:
            USBTemps=""

        #watts = randint(0,8000)
        frontroom = 66.00
        bedroom = 66.00
        kitchen = 66.00
        external = 66.00     
        watts = decodexml.decodexml(watts)
        RTemp = raspitemp.PiTemp(RTemp)
        socketio.sleep(1)
        socketio.emit('my_response',
                      {'data':'Values', 'elec': watts,'ext': SensorValues[1],'fr': SensorValues[0],'bd': SensorValues[3],'kt': SensorValues[2]},
                      namespace='/home')


mesg = 'starting dragelec'
@app.route('/')
def index():
    today = datetime.date.today()
    templateData={
        'mesg' :mesg,
        'time' :today
    }
    return render_template('home.html', async_mode=socketio.async_mode, **templateData)

@socketio.on('connect', namespace='/home')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)

if __name__ == '__main__':

    global SensorValues
    global ser
    print("")
    print("---------------------------------------------------")
    print("---------------------------------------------------")
    print("----        STARTING DragElec MONITORING       ----")
    print("--------------- %s %s ---------------" %
          (datetime.date.today(), time.strftime("%H:%M:%S")))
    print("---------------------------------------------------")
    print("")
    ser = serial.Serial('/dev/ttyACM0', 9600)
    updateonlinetime = time.time()
    try:
        with open('/tmp/tmpvalues.csv', 'r') as csvfile:
            fileRead = csv.reader(csvfile, delimiter=',')
            for row in fileRead:
                SensorValues = [float(x) for x in row if x != '']
    except:
        SensorValues = (
            66.00,
            66.00,
            66.00,
            66.00,
            66.00,
            66.00,
            66.00,
            66.00,
            66.00,
            66.00)
    socketio.run(app, host='0.0.0.0', debug=True)
