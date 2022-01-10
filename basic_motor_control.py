#!/usr/bin/python

import serial

"""
NOTE
    This code is provided strictly 'as is'!!!
    The author makes no representations or warranties 
    regarding the code below and disclaim any liability 
    for the consequences of its use."
"""

def get_serial_oject(tinyg_usb_port):
    return serial.Serial(
        port=tinyg_usb_port,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=None,
        xonxoff=1,
        rtscts=0
    )


def run_self_test(ser, test_number):
    """
    Description:
        This script is intended to send a serial command
        to a TinyG v8 board to run a self test.
        For more information:
            https://github.com/synthetos/TinyG/wiki/Test-Drive-TinyG

    Inputs:
        ser : pyserial object
        test_number : integer
    
    Returns:
        none
    
    """
    TEST_MIN = 1
    TEST_MAX = 13

    if not (TEST_MIN <= test_number <= TEST_MAX):
        error_message = (
            f"run_test(): {test_number} is an invalid test_number.\n"\
            f"\tThe test number must be in the range {TEST_MIN} to {TEST_MAX}."
        )
        raise ValueError(error_message)
    message = f"$test={test_number}\n"
    ser.write(bytes(message, 'utf-8'))


def go_to_position(ser, speed, position):
    """
    Description:
        This script is intended demonstrate how gcode commands
        may be sent to a TinyG v8 board with Python via
        serial communication.
        The gcode command sent in a serial message will cause
        the motor connected to the TinyG Motor1 port to rotate
        at a given speed until it reaches the given position.
        
    Inputs:
        ser : pyserial object
        speed : integer
        position : integer
    
    Returns:
        none
    
    Remarks:
        TODO The speed and position ranges need to be specified.
    
    """
    message = f'g1 f{speed} x{position}\n'
    ser.write(bytes(message, 'utf-8'))


def red_text(original_text):
    return f"\033[31m{original_text}\033[0m"

def main():
    # TODO The port must be set to the USB port that the TinyG is connected to.
    ser = get_serial_oject('/dev/ttyUSB0')

    message = (
        f"\n{red_text('---CAUTION!!!---')}\n"\
        "THIS PROGRAM WILL ACTIVATE TINYG MOTOR 1.\n"\
        "ENSURE THAT MOTOR WILL OPERATE SAFELY BEFORE CONTINUING.\n\n"\
        "Enter 1 to continue, or enter to quit."
    )
    user_response = input(message)
    if user_response.lower() != "1":
        exit()
    
    speed = input("Enter a motor speed (E.g., 50):")
    position = input("Enter a position (E.g., 100):")

    go_to_position(ser, speed, position)
    

    
if __name__ == '__main__':
    main()