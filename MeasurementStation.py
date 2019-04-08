import time
import board
import busio
import adafruit_bme280
import RPi.GPIO as GPIO


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
        pass
    def continuousMeasurement(self):
        pass

    def collectMeasurements(self):

        pass

    def sendMeasurements(self):
        pass


class Bed(object):
    def __init__(self, bedName):
        self.bedName = bedName
        self.sensorList = []

    def addSensor(self, sensor):
        self.sensorList.append(sensor)

    def collectMeasurements(self):
        measurementList = [] #todo: is just list, has to be changed to dict Type:value
        for x in range(0, len(self.sensorList)):    #for all sensors
            for y in range(0, len(self.sensorList[x].measurementTypeList)):     #for all measurementTypes
                measurementList.append(self.sensorList[x].measure(self.sensorList[x].measurementTypeList[y]))
            #todo: only measures temperature

        return measurementList


class Sensor(object):

    def __init__(self, measurementType, pinDictionary):
        self.measurementType = measurementType
        self.pinDictionary = pinDictionary

    def measure(self, measurementType):
        return SensorMeasurement

class BME_280_Sensor(Sensor):


    def __init__(self, measurementTypeList, pinDictionary):
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
            return SensorMeasurement("dewPoint", self.bme280.temperature - ((100-self.bme280.humidity) / 5), time.asctime())

        else:
            print("add exception here")
            #todo: add throw exception

#test

myGarden = Garden("addr", "pw", "name", 5)
myGarden.addBed(Bed("bedOne"))

myBed = Bed("firstBed")
myBed.addSensor(BME_280_Sensor(["temperature", "humidity"], ""))
measurements = myBed.collectMeasurements()
for i in range(0, len(measurements)):
    print(measurements[i].measurementValue)