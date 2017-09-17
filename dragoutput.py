#!/usr/bin/env python
# start of creating a single output module for all uses
# NOT TESTED OR USED

import datetime
import time
import logging
import logging.handlers
import csv
import MySQLdb


def dragreadcsv():
    # read in stored values
    try:
        with open('/tmp/tmpvalues.csv', 'r') as csvfile:
            fileRead = csv.reader(csvfile, delimiter=',')
            for row in fileRead:
                # SensorValues = row

                new = [float(x) for x in row if x != '']
                SensorValues = ','.join(new)
                print(SensorValues)
    except:
        SensorValues = (
            18.55,
            9.66,
            17.69,
            18.19,
            43.06,
            3.16,
            3.11,
            2.27,
            2.46,
            2.71)
        # finally:
        # csvfile.close()
    pass


def dragwritecsv():
    # write sensor values to temp file for retrieval .. maybe able to read
    # from sqldb in future
    try:
        with open('/tmp/tmpvalues.csv', 'wb') as csvfile:
            fileWrite = csv.writer(csvfile, delimiter=',', quotechar='|')
            fileWrite.writerow(SensorValues)
    finally:
        csvfile.close()
v pass


def draglog():
    # logfile handling section
    loghandler = logging.handlers.TimedRotatingFileHandler(
        "/media/nas_documents/elec_logfiles/DragElec", when="w6")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(loghandler)
    logger.info(
        "%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f" %
        (time.strftime("%d/%m/%Y"),
         time.strftime("%H:%M:%S"),
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
    pass


def dragsql():
    # setup MySQLdb connection
    db = MySQLdb.connect("localhost", "monitor", "password", "sensors")
    curs = db.cursor()
    # output to mysql database
    with db:
        curs.execute(
            "INSERT INTO tdat values(CURRENT_DATE(), NOW(), 'frontroom', %s)",
            SensorValues[0])
        curs.execute(
            "INSERT INTO tdat values(CURRENT_DATE(), NOW(), 'kitchen', %s)",
            SensorValues[2])
        curs.execute(
            "INSERT INTO tdat values(CURRENT_DATE(), NOW(), 'bedroom', %s)",
            SensorValues[3])
        curs.execute(
            "INSERT INTO tdat values(CURRENT_DATE(), NOW(), 'external', %s)",
            SensorValues[1])
        curs.execute(
            "INSERT INTO tdat values(CURRENT_DATE(), NOW(), 'light', %s)",
            SensorValues[4])
    pass
