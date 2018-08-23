# !/usr/bin/env python
import raspitemp  # Raspberry CPU Temp reader
import decodesensor # reads wireless sensors
import decodexml  # reads & decodes the currentcost xml string
import datetime, time
import serial
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from random import randint
import pdb
import sqlite3
from pathlib import Path

# (aABTEMP,aACTEMP,aADTEMP,aAETEMP,aAZLIGHT,aABBATT,aACBATT,aADBATT,aAEBATT,aAZBATT)
# AE - Bedroom, AB - Front room,AD - Kitchen,AC - External,AZ - Light level

#SensorValues = (0,0,0,0,0,0,0,0,0,0)

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

def background_thread():
    llapMsg = ""
    RTemp = 0
    sensordict = {'msg':llapMsg,'AB':0,'AC':1,'AD':2,'AE':3,'AZ':4}
    global ser
    global SensorValues
    
    while True:
        n = ser.inWaiting()
        if n != 0:
            llapMsg= ser.read(n)
            d_now = datetime.datetime.now().strftime('%Y-%m-%d')
            t_now = datetime.datetime.now().strftime('%H:%M:%S')
            sensordict['msg']=(llapMsg.decode('utf8'))
            sensordict = decodesensor.decdict(sensordict)
            print("MSG RXD: ", llapMsg, "data:", sensordict)
            tn = 'home_mon'
            # Connecting to the database file
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("INSERT INTO {tn}(DATE,TIME,EXTERNAL,FRONTROOM,BEDROOM,KITCHEN) VALUES(?,?,?,?,?,?)".format(tn='home_mon'), (d_now, t_now, sensordict.get('AC'), sensordict.get('AB'), sensordict.get('AE'), sensordict.get('AD')))
            conn.commit()
            conn.close()

        else:
            llapMsg = ""

        RTemp = raspitemp.PiTemp(RTemp)
        socketio.sleep(1)
        socketio.emit('my_response',
                      {'data':'Values', 'ext': sensordict.get('AC'),'fr': sensordict.get('AB'),'bd': sensordict.get('AE'),'kt': sensordict.get('AD')},
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
    sqlite_file = '/mnt/usbkey/home_mon_db.sqlite'
    myfile = Path(sqlite_file)
    if myfile.is_file():
        # file exists
        print('file exists')
    else:
        tn = 'home_mon'
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        # create table
        c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY AUTOINCREMENT)'.format(tn='home_mon', nf='IDX', ft='INTEGER') )
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='home_mon', cn="DATE", ct='DATE'))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='home_mon', cn="TIME", ct='TIME'))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='home_mon', cn="EXTERNAL", ct='REAL'))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='home_mon', cn="FRONTROOM", ct='REAL'))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='home_mon', cn="BEDROOM", ct='REAL'))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='home_mon', cn="KITCHEN", ct='REAL'))

    # sensordict = {'msg':llapMsg,'AB':0,'AC':2,'AD':0,'AE':0,'AZ':0}
    updateonlinetime = time.time()

    socketio.run(app, host='0.0.0.0', debug=True)
