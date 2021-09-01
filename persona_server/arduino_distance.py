import serial

#port = "/dev/tty.usbmodem1411"  # On Mac/Linux
port = "COM3"  # On Windows


def return_arduino_distance(port=port):
    ser = serial.Serial(port)
    string = ser.readline()
    numbers = []
    for word in string.split():
        if word.isdigit():
            numbers.append(int(word))
    n = numbers[0]
    if 0 <= n < 75:
        reaction = 'd40'
    elif 75 <= n < 150:
        reaction = 'd75'
    elif 150 <= n < 230:
        reaction = 'd150'
    else:
        reaction = 'd200'
    return reaction

if __name__ == '__main__':
    while True:
        print(return_arduino_distance(port))


