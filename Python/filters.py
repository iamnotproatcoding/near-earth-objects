import operator


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __call__(self, approach):
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"
   
class DateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.time.date()

class DistanceFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.distance
    
class VelocityFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.velocity
    
class DiameterFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous

def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    filters = []
    
    if date:
        filters.append(DateFilter(operator.eq, date))
    if start_date:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max:
        filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max:
        filters.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))

    return filters


def limit(iterator, n=None):
    if n == 0 or n is None:
        return iterator
    return [x for i, x in enumerate(iterator) if i < n]