# ----------------------------------
# emaildrag.py
# Version 0.1
# ----------------------------------
import smtplib
from email.mime.text import MIMEText
import time
import credentials


def PrepMail(
        alert,
        Duration,
        AvgWatts,
        Cost,
        aABTEMP,
        aACTEMP,
        aADTEMP,
        aAETEMP,
        aAZLIGHT):

    # debug = 1
    smtpdata = credentials.em_login['smtpdata']
    emlogin = credentials.em_login['login']
    empassword = credentials.em_login['password']
    toemail = credentials.em_login['toemail']

    if alert == 1:
        # ----------------------------------
        # shower length alert
        # ----------------------------------
        NowTime = time.strftime("%H:%M:%S")
        NowDate = NowDate = (time.strftime("%d/%m/%Y"))
        # message = "%s \n %s \n Duration:%.0f \n AvgWatts:%.1f \n Cost:%.1f" \
        # % (NowDate,NowTime,Duration,AvgWatts,Cost)
        message = "%s \n %s \n Duration:%.0f \n AvgWatts:%.1f \n Cost:%.1f \n \
        Temperatures at the time: \n \n Frontroom:%.2f : Kitchen:%.2f : \
        Bedroom:%.2f : External:%.2f : Light level:%.2f" % (
            NowDate,
            NowTime,
            Duration,
            AvgWatts,
            Cost,
            aABTEMP,
            aADTEMP,
            aAETEMP,
            aACTEMP,
            aAZLIGHT)
        msg = MIMEText(message)
        msg['Subject'] = 'DragElec - Duration: %.2f - Cost - %0.2f' % (
            Duration, Cost)
        msg['From'] = emlogin
        msg['To'] = toemail
        # print("Shower length alert:%.0f - AvgWatts:%.2f - Duration:%.2f - \
        # Cost:%.2f" % (alert, AvgWatts, Duration, Cost))
        status = 1
        alert = 0
    pass

    if alert == 2:
        # ----------------------------------
        # dragon cage temp warning
        # ----------------------------------
        # message = "Warning DragonTemp Low - %.2f " % (DragonTemp)
        # msg = MIMEText (message)
        # msg['Subject'] = 'WARNING: DRAGON TEMPERATURE: %.2f' % (DragonTemp)
        # msg['From'] = emlogin
        # msg['To'] = toemail
        status = 2
        print("DRAGON temp alert %.0f" % alert)
    pass

    if alert == 3:
        # ----------------------------------
        # Daily status report
        # ----------------------------------
        # daily status email
        # message = "Daily status"
        # msg = MIMEText (message)
        # msg['Subject'] = 'Daily status' % (DragonTemp)
        # msg['From'] = emlogin
        # msg['To'] = toemail
        status = 3
        print("Daily status %.0f" % alert)
    pass

    if alert == 4:
        # ----------------------------------
        # battery low alert
        # ----------------------------------
        NowTime = time.strftime("%H:%M:%S")
        NowDate = NowDate = (time.strftime("%d/%m/%Y"))
        message = "%s \n %s \n %s" % (
            NowDate,
            NowTime,
            AvgWatts)
        msg = MIMEText(message)
        msg['Subject'] = 'SENSOR BATTERY LOW'
        msg['From'] = emlogin
        msg['To'] = toemail
        status = 4
        print("Battery low msg: %s" % Duration)
    pass

    if status == 1 or status == 2 or status == 3 or status == 4:
        try:
            s = smtplib.SMTP(smtpdata)
            s.login(emlogin, empassword)
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()
            print("Mail sent ok")
            status = 666
        except Exception:
            print("Error sending mail")
            status = 999

    return(status)
