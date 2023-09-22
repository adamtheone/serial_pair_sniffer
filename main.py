import time

import serial
from datetime import datetime

# SETUP ------------------
PORT1_NAME = "COM23"
PORT1_BAUD = 115200

PORT2_NAME = "COM10"
PORT2_BAUD = 115200

PRINTING_ENABLED = True
# ------------------------

TIMEOUT = 1 / 1000  # 1ms should give 115bytes at 115200baud

def main():
    serial1 = serial.Serial()
    serial1.port = PORT1_NAME
    serial1.baudrate = PORT1_BAUD
    serial1.timeout = 0.001

    serial2 = serial.Serial()
    serial2.port = PORT2_NAME
    serial2.baudrate = PORT2_BAUD
    serial2.timeout = 0.001
    try:
        serial1.open()
        serial2.open()
    except serial.serialutil.SerialException as e:
        print(f'Cannot open the serial port(s): {PORT1_NAME}, {PORT2_NAME}. Error: {e}')
        return

    print(f'Connected to ports: {PORT1_NAME}, {PORT2_NAME}')

    last_rx_time = time.time()
    while True:
        try:
            data1 = serial1.read(100)
            if len(data1):
                serial2.write(data1)
                last_rx_time = time.time()
                if PRINTING_ENABLED:
                    print(f'[{datetime.now().strftime("%H:%M:%S.%f")[:-3]}] >> {data1}')    # .decode("utf-8")}')
            data2 = serial2.read(100)
            if len(data2):
                serial1.write(data2)
                last_rx_time = time.time()
                if PRINTING_ENABLED:
                    print(f'[{datetime.now().strftime("%H:%M:%S.%f")[:-3]}] << {data2}')    # .decode("utf-8")}')
        except:
            pass

        if last_rx_time and time.time() - last_rx_time > 0.5:
            last_rx_time = 0
            print()


if __name__ == '__main__':
    main()
