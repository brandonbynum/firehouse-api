import datetime

def dateToStringConverter(o):
  if isinstance(o, datetime.datetime):
      return o.__str__()