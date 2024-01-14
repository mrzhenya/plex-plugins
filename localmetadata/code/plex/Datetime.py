import datetime, re, time

def ParseDate(date, fmt=None):
  """
    Attempts to convert the given string into a datetime object.

    :type date: str

    :rtype: `datetime <http://docs.python.org/library/datetime.html#datetime-objects>`_
  """
  if date == None or len(date) == 0:
    return None #TODO: Should we return None or throw an exception here?
  try:
    year_only = re.compile(r'[0-9]{4}')
    year_month_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    if fmt != None:
      result = datetime.datetime.strptime(date, fmt)
    elif year_month_date.match(date):
      result = datetime.datetime.strptime(date, "%Y-%m-%d")
    elif year_only.match(date):
      result = datetime.datetime.strptime(date + '-01-01', "%Y-%m-%d")
    else:
      result = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(date)))
  except:
    return None # Zhenya - this is a non-handled case here
  return result
