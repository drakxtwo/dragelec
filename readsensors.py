# ----------------------------------
# reads wireless sensors
# ----------------------------------


def readWireless(
        aABTEMP,
        aACTEMP,
        aADTEMP,
        aAETEMP,
        aAZLIGHT,
        aABBATT,
        aACBATT,
        aADBATT,
        aAEBATT,
        aAZBATT):
    import serial
    import time
    debug = 0

    USBTemps = serial.Serial('/dev/ttyACM0', 38400)

    time.sleep(0.5)
    if USBTemps.inWaiting() > 0:
        llapMsg = USBTemps.read(USBTemps.inWaiting())
        # decode from bytes to string
        llapMsg = llapMsg.decode(encoding='UTF-8')

        if debug == 1:
            print(len(llapMsg), llapMsg)
        if len(llapMsg) == 12 or len(llapMsg) == 36 or len(llapMsg) == 48:
            sensorValues = valueCheck(
                llapMsg,
                aABTEMP,
                aACTEMP,
                aADTEMP,
                aAETEMP,
                aAZLIGHT,
                aABBATT,
                aACBATT,
                aADBATT,
                aAEBATT,
                aAZBATT)
        else:
            print("need to debug message received: ", len(llapMsg), llapMsg)
            sensorValues = (
                aABTEMP,
                aACTEMP,
                aADTEMP,
                aAETEMP,
                aAZLIGHT,
                aABBATT,
                aACBATT,
                aADBATT,
                aAEBATT,
                aAZBATT)
            # battcheck(llapMsg)
    else:
        sensorValues = (
            aABTEMP,
            aACTEMP,
            aADTEMP,
            aAETEMP,
            aAZLIGHT,
            aABBATT,
            aACBATT,
            aADBATT,
            aAEBATT,
            aAZBATT)

    return (
            sensorValues[0],
            sensorValues[1],
            sensorValues[2],
            sensorValues[3],
            sensorValues[4],
            sensorValues[5],
            sensorValues[6],
            sensorValues[7],
            sensorValues[8],
            sensorValues[9])


def valueCheck(
        llapMsg,
        aABTEMP,
        aACTEMP,
        aADTEMP,
        aAETEMP,
        aAZLIGHT,
        aABBATT,
        aACBATT,
        aADBATT,
        aAEBATT,
        aAZBATT):
    import emaildrag
    import time
    if "ABT" in llapMsg:
        # front room temp
        try:
            aABTEMP = float(llapMsg[7:12])
            print("AB temp level = %.2f - detected at %s " %
                  (aABTEMP, time.strftime("%H:%M:%S")))
        except:
            print(
                "Cannot decode - msg detected: %s - detected at %s " %
                (llapMsg, time.strftime("%H:%M:%S")))
    if "ACT" in llapMsg:
        # external temp
        try:
            aACTEMP = float(llapMsg[7:12])
            print("AC temp level = %.2f - detected at %s " %
                  (aACTEMP, time.strftime("%H:%M:%S")))
        except:
            print(
                "Cannot decode - msg detected: %s - detected at %s " %
                (llapMsg, time.strftime("%H:%M:%S")))
    if "ADT" in llapMsg:
        # kitchen temp
        try:
            aADTEMP = float(llapMsg[7:12])
            print("AD temp level = %.2f - detected at %s " %
                  (aADTEMP, time.strftime("%H:%M:%S")))
        except:
            print(
                "Cannot decode - msg detected: %s - detected at %s " %
                (llapMsg, time.strftime("%H:%M:%S")))
    if "AET" in llapMsg:
        # bedroom temp
        try:
            aAETEMP = float(llapMsg[7:12])
            print("AE temp level = %.2f - detected at %s " %
                  (aAETEMP, time.strftime("%H:%M:%S")))
        except:
            print(
                "Cannot decode - msg detected: %s - detected at %s " %
                (llapMsg, time.strftime("%H:%M:%S")))
    # light level sensor
    if "AZL" in llapMsg:
        # bedroom temp
        try:
            aAZLIGHT = float(llapMsg[7:12])
            print("AZ light level = %.2f - detected at %s " %
                  (aAZLIGHT, time.strftime("%H:%M:%S")))
        except:
            print(
                "Cannot decode - msg detected: %s - detected at %s " %
                (llapMsg, time.strftime("%H:%M:%S")))

    if "ABB" in llapMsg:
        try:
            aABBATT = float(llapMsg[31:35])
            print(
                "AB Battery level = %.2f - detected at %s " %
                (aABBATT, time.strftime("%H:%M:%S")))
        except ValueError:
            print("aABBATT Conversion ERROR:", llapMsg)

    if "ACB" in llapMsg:
        try:
            aACBATT = float(llapMsg[31:35])
            print(
                "AC Battery level = %.2f - detected at %s " %
                (aACBATT, time.strftime("%H:%M:%S")))
        except ValueError:
            print("aACBATT Conversion ERROR:", llapMsg)

    if "ADB" in llapMsg:
        try:
            aADBATT = float(llapMsg[31:35])
            print(
                "AD Battery level = %.2f - detected at %s " %
                (aADBATT, time.strftime("%H:%M:%S")))
        except ValueError:
            print("aADBATT Conversion ERROR:", llapMsg)

    if "AEB" in llapMsg:
        try:
            aAEBATT = float(llapMsg[31:35])
            print(
                "AE Battery level = %.2f - detected at %s " %
                (aAEBATT, time.strftime("%H:%M:%S")))
        except ValueError:
            print("aAEBATT Conversion ERROR:", llapMsg)

    if "AZB" in llapMsg:
        try:
            aAZBATT = float(llapMsg[31:35])
            print(
                "AZ Battery level = %.2f - detected at %s " %
                (aAZBATT, time.strftime("%H:%M:%S")))
        except ValueError:
            print("aAZBATT Conversion ERROR:", llapMsg)

    if "LOW" in llapMsg:
        if "aAB" in llapMsg:
            emaildrag.PrepMail(4, "AB BattLOW", aABBATT, 0, 0, 0, 0, 0, 0)
        if "aAC" in llapMsg:
            emaildrag.PrepMail(4, "AC BattLOW", aACBATT, 0, 0, 0, 0, 0, 0)
        if "aAD" in llapMsg:
            emaildrag.PrepMail(4, "AD BattLOW", aADBATT, 0, 0, 0, 0, 0, 0)
        if "aAE" in llapMsg:
            emaildrag.PrepMail(4, "AE BattLOW", aAEBATT, 0, 0, 0, 0, 0, 0)
        if "aAZ" in llapMsg:
            emaildrag.PrepMail(4, "AZ BattLOW", aAEBATT, 0, 0, 0, 0, 0, 0)

    return (
        aABTEMP,
        aACTEMP,
        aADTEMP,
        aAETEMP,
        aAZLIGHT,
        aABBATT,
        aACBATT,
        aADBATT,
        aAEBATT,
        aAZBATT)
