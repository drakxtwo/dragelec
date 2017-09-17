# !/usr/bin/env python

def read_csv():
    # read in stored values & initialise preset values
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

def write_csv():
    # write sensor values to temp file for retrieval
    try:
        # with python2 need 'wb' not 'w'
        with open('/tmp/tmpvalues.csv', 'wb') as csvfile:
            fileWrite = csv.writer(
                csvfile, delimiter=',', quotechar='|')
            fileWrite.writerow(SensorValues)
    finally:
        csvfile.close()
