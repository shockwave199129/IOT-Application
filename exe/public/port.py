"""This Module for geting connected serial device to mechine"""
import argparse
import sys
import json
import serial
import serial.tools.list_ports


def getSerialList() -> dict:
    """get list of serial device name and port"""

    listOfPorts = []

    ports = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(ports):
        tmp: dict = {'port': port, 'desc': desc}
        listOfPorts.append(tmp)

    return json.dumps(listOfPorts)


def readSerialOutput(port: str) -> str:
    """read serial output from serial device connected to provided port"""

    ser = serial.Serial(
        port,
        115200,
        timeout=2,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
    data_raw = ser.readline().decode('ASCII')

    return data_raw


if __name__ == "__main__":

    try:
        getopt = argparse.ArgumentParser()
        getopt.add_argument('-read', help='Read from a specific port')

        options = vars(getopt.parse_args())

        if options['read'] is None:
            sys.stdout.write(getSerialList())
        else:
            sys.stdout.write( json.dumps( {'message': readSerialOutput(options['read']) } ) )
    except Exception as ex:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        sys.stdout.write(json.dumps({'error': str(ex_value)}))
