# !/usr/bin/env python
import raspitemp  # Raspberry CPU Temp reader
import decodesensor # reads wireless sensors
import datetime, time
import serial
import sqlite3
from pathlib import Path

# (aABTEMP,aACTEMP,aADTEMP,aAETEMP,aAZLIGHT,aABBATT,aACBATT,aADBATT,aAEBATT,aAZBATT)
# AE - Bedroom, AB - Front room,AD - Kitchen,AC - External,AZ - Light level

# (aABTEMP,aACTEMP,aADTEMP,aAETEMP,aAZLIGHT,aABBATT,aACBATT,aADBATT,aAEBATT,aAZBATT)
# AE - Bedroom, AB - Front room,AD - Kitchen,AC - External,AZ - Light level
#MSG RXD:  b'aADTMPA20.36' data: {'AZ': '60.64', 'AE': '17.19', 'AD': '20.36', 'msg': 'aADTMPA20.36', 'AB': '16.78', 'AC': '2.817'}


llapMsg = ""
RTemp = 0
ser = serial.Serial('/dev/ttyACM0', 9600)
sqlite_file = '/mnt/usbkey/home_mon_db.sqlite'
myfile = Path(sqlite_file)

print("----        STARTING DragElec MONITORING       ----")
print("--------------- %s %s ---------------" %
      (datetime.date.today(), time.strftime("%H:%M:%S")))
print("")
if myfile.is_file():
    # file exists
    print('file exists')
    conn=sqlite3.connect('home_mon_db.sqlite')
    curs=conn.cursor()
    pd.set_option('display.max_rows', None)
    df = pd.read_sql_query("select * from home_mon order by IDX desc limit 1;", conn)
    AC=(df.iloc[0][3]) #external temp
    AB=(df.iloc[0][4]) #frontroom temp
    AE=(df.iloc[0][5]) #bedroom temp
    AD=(df.iloc[0][6]) #kitchen temp
    AZ=0 # not stored in db
    sensordict = {'msg':llapMsg,'AB':AB,'AC':AC,'AD':AD,'AE':AE,'AZ':86.76}
    conn.close()
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



while 0:
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
