"""DOCSTRING

"""
import time
import board
import busio
import adafruit_bme280
import psycopg2
# import RPi.GPIO as GPIO


class SensorMeasurement(object):

    def __init__(self, measurementType, measurementValue, measurementTime):
        self.measurementType = measurementType
        self.measurementValue = measurementValue
        self.measurementTime = measurementTime
        self.bedName = ""
        self.gardenName = ""


class Garden(object):
    def __init__(self, databaseAddress, databaseUser, databasePassword, tableName, gardenName, measurementFrequency):
        self.databaseAddress = databaseAddress
        self.databaseUser = databaseUser
        self.databasePassword = databasePassword
        self.tableName = tableName
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
        for x in range(0, len(self.bedList)):  # for every bed
            bedMeasurementList = (self.bedList[x].collectMeasurements())  # collect all measurements
            for y in range(0, len(bedMeasurementList)):  # for every measurement
                bedMeasurementList[y].gardenName = self.gardenName  # add gardenName to measurement
                gardenMeasurementList.append(bedMeasurementList[y])  # add measurement to list

        return gardenMeasurementList

    def sendMeasurements(self, measurements):
        for i in range(0, len(measurements)):
            print(str(measurements[i].measurementTime) + ": " +
                  measurements[i].measurementType + ": " +
                  str(measurements[i].measurementValue))
        print("---")

        conn = psycopg2.connect('host={} user={} password={} dbname={}'
                                .format(self.databaseAddress, self.databaseUser, self.databasePassword, self.tableName))
        cursor = conn.cursor()
        query = "INSERT INTO measurements(measurementtime, measurementtype, measurementvalue, bedname, gardenname) " \
                "VALUES (%s, %s, %s, %s, %s)"
        for measurement in measurements:
            values = (measurement.measurementTime, measurement.measurementType, measurement.measurementValue,
                      measurement.bedName, measurement.gardenName)
            cursor.execute(query, values)
            conn.commit()
        conn.close()
        cursor.close()


class Bed(object):
    def __init__(self, bedName):
        self.bedName = bedName
        self.sensorList = []

    def addSensor(self, sensor):
        self.sensorList.append(sensor)

    def collectMeasurements(self):
        bedMeasurementList = []  # is list of type SensorMeasurement
        for x in range(0, len(self.sensorList)):  # for every sensor
            for y in range(0, len(self.sensorList[x].measurementTypeList)):  # for every measurementType
                newMeasurement = self.sensorList[x].measure(self.sensorList[x].measurementTypeList[y])  # measure sensor
                newMeasurement.bedName = self.bedName  # add bedName to measurement
                bedMeasurementList.append(newMeasurement)  # add measurement to list

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

        elif measurementType == "airHumidity":
            return SensorMeasurement("airHumidity", self.bme280.humidity, time.asctime())

        elif measurementType == "pressure":
            return SensorMeasurement("pressure", self.bme280.pressure, time.asctime())

        elif measurementType == "dewPoint":
            return SensorMeasurement("dewPoint", self.bme280.temperature - ((100-self.bme280.humidity) / 5),
                                     time.asctime())

        else:
            print("add exception here")
            # todo: add throw exception
