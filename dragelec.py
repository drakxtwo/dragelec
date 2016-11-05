
# !/usr/bin/env python
# DragElec_Main.py


# import readWiredTemp ;# reads DS18B20 sensor
# import updateonline ;# updates online eg plotly
# import dragoutput ;# handles csv read/write, log files, mysql
import emaildrag  # sends alert emails
import raspitemp  # Raspberry CPU Temp reader
import readsensors  # reads wireless sensors
import decodexml  # reads & decodes the currentcost xml string
import datetime
import time
import logging
import logging.handlers
import csv
import credentials
from ISStreamer.Streamer import Streamer

debug = 0

# (aABTEMP,aACTEMP,aADTEMP,aAETEMP,aAZLIGHT,aABBATT,aACBATT,aADBATT,aAEBATT,aAZBATT)
# AE - Bedroom, AB - Front room,AD - Kitchen,AC - External,AZ - Light level

# set up initial state streamer
b_name = credentials.in_login['bucketname']
b_key = credentials.in_login['bucketkey']
a_key = credentials.in_login['accesskey']
if debug == 1:
    print(b_name, b_key, a_key)
streamer = Streamer(bucket_name=b_name, bucket_key=b_key,
                    access_key=a_key, debug_level=0)


# logfile handling section
loghandler = logging.handlers.TimedRotatingFileHandler(
    "/media/nas_documents/elec_logfiles/DragElec", when="w6")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(loghandler)

# read in stored values & initialise preset values
try:
    with open('/tmp/tmpvalues.csv', 'r') as csvfile:
        fileRead = csv.reader(csvfile, delimiter=',')
        for row in fileRead:
            SensorValues = [float(x) for x in row if x != '']
except:
    SensorValues = (
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,
        2.00)

HighWatts = 5000
LowWatts = 2000
watts = TotalWatts = HiDuration = HighStart = AvgWatts = cost = RTemp = 0
updateonlinetime = time.time()

if debug == 1:
    print(SensorValues)
    print("HighWatts:%.0f LowWatts:%.0f"
          "updateonlinetime:%.0f") % (HighWatts, LowWatts, updateonlinetime)

print("")
print("---------------------------------------------------")
print("---------------------------------------------------")
print("----        STARTING DragElec MONITORING       ----")
print("--------------- %s %s ---------------" %
      (datetime.date.today(), time.strftime("%H:%M:%S")))
print("---------------------------------------------------")
print("")
try:
    while True:
        time.sleep(1)
        today = datetime.date.today()
        # aABTEMP,aACTEMP,aADTEMP,aAETEMP,aAZLIGHT, /
        # aABBATT,aACBATT,aADBATT,aAEBATT,aAZBATT)
        SensorValues = readsensors.readWireless(
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
        watts = decodexml.decodexml(watts)
        RTemp = raspitemp.PiTemp(RTemp)
        print(
            "%s-%s: Rpi:%.1f Watts:%.1f - FR:%.2f-EXT:%.2f-KT:%.2f"
            "-BD:%.2f-Light:%.2f" %
            (today,
             time.strftime("%H:%M:%S"),
             RTemp,
             watts,
             SensorValues[0],
             SensorValues[1],
             SensorValues[2],
             SensorValues[3],
             SensorValues[4]))

        if watts > HighWatts:
            TotalWatts = TotalWatts + watts
            if HighStart == 0:
                HighStart = time.time()
        if HighStart != 0 and watts < LowWatts:
            if HiDuration > 300:
                # calculate time in seconds
                HiDuration = int(time.time() - HighStart)
                # calculate average watts used
                AvgWatts = TotalWatts / (HiDuration / 6)
                # calculate kilowatt-hours
                kWH = (AvgWatts / 1000) * (HiDuration / 3600)
                cost = kWH * 0.1618  # cost of kilowatt-hours
                if debug == 1:
                    # print("Start:%.2f - Duration:%.2f - End:%.2f" %
                    #      (HighStart, HiDuration, int(time.time())))
                    pass
                mailSent = emaildrag.PrepMail(
                    1,
                    HiDuration,
                    AvgWatts,
                    cost,
                    SensorValues[0],
                    SensorValues[1],
                    SensorValues[2],
                    SensorValues[3],
                    SensorValues[4])
                print("Mail sent msg: ", mailSent)
                TotalWatts = HiDuration = HighStart = AvgWatts = cost = 0
            else:
                TotalWatts = HiDuration = HighStart = AvgWatts = cost = 0
        if time.time() > updateonlinetime + 14400:
            updateonlinetime = time.time()
            # output to online service
            # onlineResponse = updateonline.updateThingspeak(
            # SensorValues[0],SensorValues[1],SensorValues[2],SensorValues[3])
            # output to logfile
            print("Output to sources")
            logger.info(
                "%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,"
                "%.2f,%.2f,%.2f" %
                (time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"),
                    RTemp,
                    watts,
                    SensorValues[0],
                    SensorValues[1],
                    SensorValues[2],
                    SensorValues[3],
                    SensorValues[4],
                    SensorValues[5],
                    SensorValues[6],
                    SensorValues[7],
                    SensorValues[8],
                    SensorValues[9]))

            # update initial state
            streamer.log("Front room", SensorValues[0])
            streamer.log("Kitchen", SensorValues[2])
            streamer.log("Bedroom", SensorValues[3])
            streamer.log("External", SensorValues[1])
            streamer.flush()
            # write sensor values to temp file for retrieval
            try:
                # with python2 need 'wb' not 'w'
                with open('/tmp/tmpvalues.csv', 'wb') as csvfile:
                    fileWrite = csv.writer(
                        csvfile, delimiter=',', quotechar='|')
                    fileWrite.writerow(SensorValues)
            finally:
                csvfile.close()

except KeyboardInterrupt:
    streamer.close()
    print("  Quit")
