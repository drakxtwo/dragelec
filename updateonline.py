# ----------------------------------
# updateOnline.py
# Version 0.2
# ----------------------------------


def updatePlotly(date, temp):
    py = plotly.plotly(username='username', key='key')
    r = py.plot(date, electricity,
                filename='electricity',
                fileopt='extend',
                layout={'title': 'Electricty Consumption'})


def updateThingspeak(aABTEMP, aACTEMP, aADTEMP, aAETEMP):
    import http.client
    import urllib.parse  # python 3 specific
    params = urllib.parse.urlencode(
        {'field1': aABTEMP, 'field2': aACTEMP, 'field3': aADTEMP, 'field4': aAETEMP})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update?key=2PG1ZY9KAPTLJ8OM", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print("Updated online successfully: ", response)
        # return (response.status,response.data)
    except:
        # print("Error updating thingspeak")
        pass
