import serial

port = "/dev/tty.usbmodem1411"
#port = "modem1411"

def return_arduino_distance():
    ser = serial.Serial(port)
    while True:
        string = ser.readline()
        numbers = []
        for word in string.split():
            if word.isdigit():
                numbers.append(int(word))
        n = numbers[0]
        if 0<= n < 40:
            reaction = 'd40'
        elif 40 <= n < 75:
            reaction = 'd75'
        elif 75 <= n < 150:
            reaction = 'd150'
        else:
            reaction = 'd200'
        return reaction

if __name__ == '__main__':
    while True:
        print(return_arduino_distance())


