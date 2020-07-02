    # I know it allways return False the first time, but this is easier and makes sure conection is made
    # and the slight delay this makes don't realy matter.
    wlan1.connect(ESSID, Password)
    time_at_connect = utime.ticks_ms()
    while wlan1.isconnected() == False:
        pass
        if utime.ticks_diff(time_at_connect, utime.ticks_ms()) > 60000:
            print('Network error can not connect')
            break
    
