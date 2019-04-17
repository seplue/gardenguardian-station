from MeasurementStation import *

# test
"""Test """

myGarden = Garden("addr", "pi", "pw", "name", 60)
myBed = Bed("firstBed")
myBed.addSensor(BME_280_Sensor(["temperature", "airHumidity", "pressure", "dewPoint"], ""))
myGarden.addBed(myBed)

myMeasurements = myGarden.collectMeasurements()
myGarden.sendMeasurements(myMeasurements)

#myGarden.continuousMeasurement(60)
