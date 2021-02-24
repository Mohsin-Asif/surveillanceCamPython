from datetime import datetime
import time


def timestamp():
    dt=datetime.now()
    dt=dt.strftime("%Y-%m-%d-%H-%M-%S")
    return dt

print(f'output_{timestamp()}.avi')
