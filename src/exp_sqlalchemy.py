from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from datetime import datetime
from src.models import Measurement

Base = declarative_base()
#create engine
engine = create_engine('sqlite:///gg_station_test.db', echo=True)
# for creating the db file.
# Base.metadata.create_all(engine)

# make session
Session = sessionmaker(bind=engine)
session = Session()


def sendMeasurements():
    """
    # print measurements to be sent
    print("gardenName" + ": " + measurements[0].gardenName)
    print("bedName" + ": " + measurements[0].bedName)
    for i in range(0, len(measurements)):
        print(str(measurements[i].measurementTime) + ": " +
              measurements[i].measurementType + ": " +
              str(measurements[i].measurementValue))
"""
    m1 = Measurement(
        measurement_time=datetime.utcnow(),
        measurement_type="Pressure",
        measurement_value=966,
        bed_name="mybed",
        garden_name="mygarden"
    )
    session.add(m1)
    session.commit()

    print("records inserted.")