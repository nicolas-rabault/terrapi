import sys
import time
import Adafruit_DHT

class humidity:
    """this class give access to humidity sensor"""

    def __init__(self, sensorType, pinNumber):
        #TODO take it from pypot config file
        # Sensor should be set to DHT11, DHT22, or .AM2302.
        self.sensor = sensorType
        #TODO take the pin number from pypot config file
        self.pin = pinNumber

        #TODO take the offset values from pypot config file
        self.humidityOffset = 0
        self.temperatureOffset = 0

        self.humidity = 0
        self.temperature = 0

    def get_data(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        while self.humidity > 100.0:
            time.sleep(2)
            self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        self.humidity = self.humidity + self.humidityOffset
        self.temperature = self.temperature + self.temperatureOffset

    def calibration(self, realTemperature, realHumidity):
        # Here we catch real temperature given by user to evaluate delta between
        # real life and measure from the sensor.
        self.get_data()
        self.humidityOffset = self.humidityOffset + (realHumidity - self.humidity)
        self.temperatureOffset = self.temperatureOffset + (realTemperature - self.temperature)

        #TODO save it on the pypot config file


    def display_data(self):

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if self.humidity != 0 and self.temperature != 0:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(self.temperature, self.humidity)
        else:
            print 'Failed to get reading. Try again!'

def main():
    # Parse command line parameters.
    sensor_args = { '11': Adafruit_DHT.DHT11,
                    '22': Adafruit_DHT.DHT22,
                    '2302': Adafruit_DHT.AM2302 }
    if len(sys.argv) < 3 or sys.argv[1] not in sensor_args:
        print 'usage: sudo python humidity.py [11|22|2302] GPIOpin#'
        print 'example: sudo python humidity.py 11 4 - Read from an DHT11 connected to GPIO #4'
        print 'If you want to run a calibration you can do : '
        print 'usage: sudo python humidity.py [11|22|2302] GPIOpin# real_temperature*C real_humidity%'
        sys.exit(1)

    sensor = humidity(sensor_args[sys.argv[1]], sys.argv[2])

    if len(sys.argv) > 3:
        if len(sys.argv) < 5:
            print 'If you want to run a calibration you can do : '
            print 'usage: sudo python humidity.py [11|22|2302] GPIOpin# real_temperature*C real_humidity%'
            sys.exit(1)
        sensor.calibration(float(sys.argv[3]), float(sys.argv[4]))

    sensor.get_data()
    sensor.display_data()


if __name__ == "__main__":
    main()
