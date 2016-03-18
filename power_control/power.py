import RPi.GPIO as GPIO
import time

class power:
    """this class give access to power contactor"""

    def __init__(self, deviceList):
        self.normal = {'normalOpen' : 0,
                       'normalClose' : 1}
        # devicelist is formated like
        # 'device name': [pinNumber, normal ('normalOpen' or 'normalClose')]
        self.deviceList = deviceList
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for item in self.deviceList:
            GPIO.setup(self.deviceList[item][0],GPIO.OUT)

    def enable(self, device):
        if self.deviceList[device][1] == 'normalOpen' :
            GPIO.output(self.deviceList[device][0],
                        GPIO.HIGH)
        else:
            GPIO.output(self.deviceList[device][0],
                        GPIO.LOW)

    def disable(self, device):
        if self.deviceList[device][1] == 'normalClose' :
            GPIO.output(self.deviceList[device][0],
                        GPIO.HIGH)
        else:
            GPIO.output(self.deviceList[device][0],
                        GPIO.LOW)


def main():

    # This list should be stored on the pypot config file
    devices = {'foger': [4, 'normalOpen'],
               'mainPump': [14, 'normalOpen'],
               'rain': [3, 'normalClose'] }

    power_controler = power(devices)

    power_controler.enable('foger')
    time.sleep(0.2)
    power_controler.enable('mainPump')
    time.sleep(0.2)
    power_controler.enable('rain')
    time.sleep(0.2)
    power_controler.disable('foger')
    time.sleep(0.2)
    power_controler.disable('mainPump')
    time.sleep(0.2)
    power_controler.disable('rain')
    time.sleep(0.2)


if __name__ == "__main__":
    main()
