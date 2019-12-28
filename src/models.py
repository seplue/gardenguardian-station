from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'measurement'

    id = Column(Integer, primary_key=True)
    measurement_time = Column(DateTime)
    measurement_type = Column(String(100))
    measurement_value = Column(Float)
    bed_name = Column(String(100))
    garden_name = Column(String(100))

    def __repr__(self):
        return "Measurement({} {} {} {} {} {})".format(
            self.id, self.measurement_time, self.measurement_type,
            self.measurement_value, self.bed_name, self.garden_name)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id':                self.id,
           "measurement_time":  self.measurement_time,
           "measurement_type":  self.measurement_type,
           "measurement_value": self.measurement_value,
           "bed_name":          self.bed_name,
           "garden_name":       self.garden_name
        }
