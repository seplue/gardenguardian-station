import time
import board
import busio
import adafruit_bme280
# import RPi.GPIO as GPIO


class SensorMeasurement(object):

    def __init__(self, measurementType, measurementValue, measurementTime):
        self.measurementType = measurementType
        self.measurementValue = measurementValue
        self.measurementTime = measurementTime


class Garden(object):
    def __init__(self, databaseAddress, databasePassword, gardenName, measurementFrequency):
        self.databaseAddress = databaseAddress
        self.databasePassword = databasePassword
        self.gardenName = gardenName
        self.measurementFrequency = measurementFrequency
        self.bedList = []

    def addBed(self, bed):
        self.bedList.append(bed)

    def continuousMeasurement(self, measurementFrequency):
        while True:
            self.sendMeasurements(self.collectMeasurements())
            time.sleep(measurementFrequency)

    def collectMeasurements(self):
        gardenMeasurementList = []  # is list of type SensorMeasurement
        for x in range(0, len(self.bedList)):
            bedMeasurementList = (self.bedList[x].collectMeasurements())
            for y in range(0, len(bedMeasurementList)):
                gardenMeasurementList.append(bedMeasurementList[y])

        return gardenMeasurementList

    @staticmethod
    def sendMeasurements(measurements):
        # todo replace print with real send method
        if True:
            for i in range(0, len(measurements)):
                print(str(measurements[i].measurementTime) + ": " +
                      measurements[i].measurementType + ": " +
                      str(measurements[i].measurementValue))
            print("---")

        pass


class Bed(object):
    def __init__(self, bedName):
        self.bedName = bedName
        self.sensorList = []

    def addSensor(self, sensor):
        self.sensorList.append(sensor)

    def collectMeasurements(self):
        bedMeasurementList = []  # is list of SensorMeasurement
        for x in range(0, len(self.sensorList)):    # for all sensors
            for y in range(0, len(self.sensorList[x].measurementTypeList)):     # for all measurementTypes
                bedMeasurementList.append(self.sensorList[x].measure(self.sensorList[x].measurementTypeList[y]))

        return bedMeasurementList


class Sensor(object):
    def __init__(self, measurementTypeList, pinDictionary):
        self.measurementType = measurementTypeList
        self.pinDictionary = pinDictionary

    def measure(self, measurementType):
        return SensorMeasurement


class BME_280_Sensor(Sensor):
    def __init__(self, measurementTypeList, pinDictionary):
        super().__init__(measurementTypeList, pinDictionary)

        self.measurementTypeList = measurementTypeList
        self.pinDictionary = pinDictionary
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c)
        # todo: change board.SCL & board.SDA to flexible pins

    def measure(self, measurementType):

        if measurementType == "temperature":
            return SensorMeasurement("temperature", self.bme280.temperature, time.asctime())

        elif measurementType == "humidity":
            return SensorMeasurement("humidity", self.bme280.humidity, time.asctime())

        elif measurementType == "pressure":
            return SensorMeasurement("pressure", self.bme280.pressure, time.asctime())

        elif measurementType == "dewPoint":
            return SensorMeasurement("dewPoint", self.bme280.temperature - ((100-self.bme280.humidity) / 5),
                                     time.asctime())

        else:
            print("add exception here")
            # todo: add throw exception


# test

myGarden = Garden("addr", "pw", "name", 5)
myBed = Bed("firstBed")
myBed.addSensor(BME_280_Sensor(["temperature", "humidity", "pressure", "dewPoint"], ""))
myGarden.addBed(myBed)

myMeasurements = myGarden.collectMeasurements()
"""
for o in range(0, len(myMeasurements)):
    print(str(myMeasurements[o].measurementTime) + ": " +
          myMeasurements[o].measurementType + ": " +
          str(myMeasurements[o].measurementValue))

print("---")"""
myGarden.continuousMeasurement(5)
