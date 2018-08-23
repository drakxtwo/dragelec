def num_chk(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def decdict(incoming):
    # print(incoming)
    # sample: aAETMPA12.45
    if incoming.get('msg') != '':
    # get sensor id from llapmsg
        id = incoming.get("msg")
        id = id[1:3]
        # get value from llapmsg
        val = incoming.get("msg")
        val = val[7:12]
        if num_chk(val)==True:
            # assign value to correct sensor in dictionary
            incoming[id] = val
        else:
            # what to do if it is not a value ?? i cant see the last value so i cant repeat it unless i move this decode into the main program [2018.08.20 17:26]
    return(incoming)
