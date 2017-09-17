#!/usr/bin/env python
def PiTemp(RTemp):
    import os
    # Return CPU temperature as a character string

    def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=", "").replace("'C\n", ""))

    temp1 = int(float(getCPUtemperature()))

    return (temp1)
