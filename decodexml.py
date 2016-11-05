# ----------------------------------
# decodeXML.py
# Version 0.1
# ----------------------------------


def decodexml(prev_watts):
    import time
    import serial
    import xml.etree.ElementTree as ET
    from xml.etree.ElementTree import ParseError
    debug = 0
    elecSER = serial.Serial('/dev/ttyUSB0', 57600)  # currentCost
    try:
        LineIn = elecSER.readline()
        if debug == 1:
            print("")
            print(LineIn)
            print("")

        CC_XML_String = ET.fromstring(LineIn)
        if CC_XML_String.find('ch1') is None:
            ch1_watts = prev_watts
        else:
            sensor = int(CC_XML_String.find('sensor').text)
            # CC_Time = (CC_XML_String.find('time').text)
            CCostTemp = float(CC_XML_String.find('tmpr').text)
            ch1 = CC_XML_String.find('ch1')
            ch1_watts = int(ch1.find('watts').text)
            if debug == 1:
                print(
                    "WattsCheck",
                    time.strftime("%H:%M:%S"),
                    sensor,
                    CCostTemp,
                    ch1_watts)
    except ParseError:
        ch1_watts = prev_watts
        print(" XML ParseError received: ", LineIn)

    return (ch1_watts)
