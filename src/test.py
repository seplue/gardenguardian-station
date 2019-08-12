from src.MeasurementStation import *

# test
"""Test """

myGarden = Garden("192.168.1.31", "gardenguardian", "Password123", "gardenguardian_test", "firstGarden", 60)
myBed = Bed("firstBed")
myBed.addSensor(BME_280_Sensor(["temperature", "airHumidity", "pressure", "dewPoint"], ""))
myGarden.addBed(myBed)


myMeasurements = myGarden.collectMeasurements()
myGarden.sendMeasurements(myMeasurements)

# myGarden.continuousMeasurement(60)
