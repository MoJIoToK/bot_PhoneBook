from datetime import datetime as dt
from time import time

def Log(data):
    time = dt.now().strftime('%d.%m.%Y %H:%M')
    with open('log.csv', 'a') as file:
        file.write('{} - {}\n'
                    .format(time, data))