from MeasurementStation import *

# test
"""Test """

myGarden = Garden("192.168.1.31", "pi", "PzFhr2017", "plantguardian_test", "firstGarden", 60)
myBed = Bed("firstBed")
myBed.addSensor(BME_280_Sensor(["temperature", "airHumidity", "pressure", "dewPoint"], ""))
myGarden.addBed(myBed)


# myMeasurements = myGarden.collectMeasurements()
# myGarden.sendMeasurements(myMeasurements)

myGarden.continuousMeasurement(60)
