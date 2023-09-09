from helpers import cd_to_datetime, datetime_to_str
import math
import datetime


class NearEarthObject:
    """ Designing the NearEarthObject class """
    def __init__(self, **info):
        """ Constructor of the class """
        self.designation = info.get("designation") # The primary designation
        self.name = info.get("name") # The IAU name --> Must resolve to a non-empty string or the None value
        self.diameter = info.get("diameter") # (in kilometers)
        if not self.diameter:
            self.diameter = float("nan") # Represents undefined diameter
        self.hazardous = info.get("hazardous") # Hazardous potential --> Must resolve a boolean
        self.approaches = [] # A collection of close approaches to Earth

    @property
    def fullname(self):
        if self.name:
            return f"{self.designation} ({self.name})" # Resolve to this if name exists
        return f"{self.designation}" # Resolve to this if not

    def __str__(self):
        """ Return a human-readable string that captures the contents of the class for a human audience """
        if not math.isnan(self.diameter):
            return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {'is' if self.hazardous else 'is not'} potentially hazardous."
        return f"NEO {self.fullname}, {'is' if self.hazardous else 'is not'} potentially hazardous."

    def __repr__(self):
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")
    
    def serialize(self):
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }

class CloseApproach:
    def __init__(self, **info):
        """ Constructor of the class """
        self._designation = info.get("designation") # The primary designation
        self.time = info.get("time") # The date and time, in UTC
        if self.time:
            self.time = cd_to_datetime(self.time)
            assert isinstance(self.time, datetime.datetime), "Date must be a datetime object"
        self.distance = info.get("distance", float("nan")) # The nominal approach distance, in astronomical units
        self.velocity = info.get("velocity", float("nan")) # The velocity, in kilometers per second
        assert isinstance(self.distance, float), "Distance must be a float object"
        assert isinstance(self.velocity, float), "Velocity must be a float object"
        self.neo = info.get("neo") # The NEO itself
        
    @property
    def designation(self):
        return self._designation

    @property
    def time_str(self):
        if self.time:
            return datetime_to_str(self.time)
        return "an unknown time"

    def __str__(self):
        """ Return a human-readable string that captures the contents of the class for a human audience """
        return f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of \
                {self.velocity:.2f} km/s."

    def __repr__(self):
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        return {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }