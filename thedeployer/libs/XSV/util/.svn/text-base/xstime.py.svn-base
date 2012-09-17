"""Hacked up W3C XML Schema datetime parsing,
reduced version of Strptime-related classes and functions.

CLASSES:
  TimeRE -- Creates regexes for pattern matching a string of text containing 
        time information as is returned by time.strftime()

FUNCTIONS:
  strptime -- Calculates the time struct represented by the passed-in string

Requires Python 2.2.1 or higher as-is.
Can be used in Python 2.2, though, if the following line is added:
  >>> True = 1; False = 0

Doesn't handle negative years, I don't think

"""
import time
import calendar
from re import compile as re_compile
from string import whitespace as whitespace_string
from types import FloatType

_months=[0,31,28,31,30,31,30,31,31,30,31,30,31]
_recType=type(re_compile(''))
              
__all__ = ['xstime']

_dict={'d': r"(?P<d>3[0-1]|[0-2]\d|\d| \d)", #The " \d" option is 
       #to make %c from ANSI
       #C work
       'H': r"(?P<H>2[0-3]|[0-1]\d|\d)",
       'm': r"(?P<m>0\d|1[0-2]|\d)",
       'M': r"(?P<M>[0-5]\d|\d)",
       'S': r"(?P<S>6[0-1]|[0-5]\d|\d)",
       's': r"(?P<s>((6[0-1]|[0-5]\d|\d)(\.\d+)))",
       'Y': r"(?P<Y>-?\d\d\d\d)",
       'Z': r"(?P<Z>(Z|[-+]\d\d:\d\d))"}

dateTimePat="%Y-%m-%dT%H:%M:(%S|%s)(%Z)?$"
datePat="%Y-%m-%d(%Z)?$"
timePat="%H:%M:(%s|%S)(%Z)?$"

class xstime:
  """Handle conversion from format directives to regexes."""
  month = day = hour = minute = second = -1
  year= tz = tzm = None
  str = None
  isDate = 0

  def __init__(self, format):
    """Convert data_string to a time struct based on the format string or re 
    object; will return an re object for format if data_string is False.

    The object passed in for format may either be an re object compiled by 
    strptime() or a format string. If False is passed in for data_string 
    then an re object for format will be returned which can be used as an 
    argument for format. The re object must be used with the same language 
    as used to compile the re object.

    """
    if isinstance(format, _recType):
      self.compiled_re = format
    else:
      self.compiled_re = self.compile(format)

  def __str__(self):
    mess=0
    if self.str is not None:
      return self.str
    if self.tz is None:
      tz=""
    elif self.isDate:
      if self.hour==0 and self.minute==0:
        tz="Z"
      elif (self.hour>12 or
          (self.hour==12 and self.minute>0)):
        s=self.second
        m=self.minute
        h=self.hour
        d=self.day
        M=self.month
        y=self.year
        self.day=self.day+1
        mess=1
        if self.minute>0:
          tz="+%02d:%02d"%(23-self.hour,60-self.minute)
        else:
          tz="+%02d:00"%(24-self.hour)
        self.minute=self.second=self.hour=0
        self._cleanup()
      else:
        tz="-%02d:%02d"%(self.hour,self.minute)
    elif self.tz==0 and self.tzm==0:
      tz="Z"
    elif self.tz>0 or (self.tz==0 and self.tzm>0):
      tz="+%02d:%02d"%(self.tz,self.tzm)
    else:
      tz="-%02d:%02d"%(-self.tz,-self.tzm)
    if self.hour>-1:
      if type(self.second)==FloatType:
        secs="%06.3f"%self.second
      else:
        secs="%02d"%self.second
    if self.month>-1:
      if self.isDate:
        self.str="%04d-%02d-%02d%s"%(self.year,self.month,self.day,tz)
        if mess:
          self.second=s
          self.minute=m
          self.hour=h
          self.day=d
          self.month=M
          self.year=y
      else:
        self.str="%04d-%02d-%02dT%02d:%02d:%s%s"%(self.year,self.month,
                                                  self.day,self.hour,
                                                  self.minute,secs,tz)
    elif self.hour>-1:
      self.str="%02d:%02d:%s%s"%(self.hour,self.minute,secs,tz)
    return self.str

  def install(self,data_string):
    found = self.compiled_re.match(data_string)
    if not found:
      raise ValueError
    for key, item in found.groupdict().iteritems():
      if key is 'Y':
        self.year = int(item)
      elif key is 'm':
        self.month = int(item)
      elif key is 'd':
        self.day = int(item)
      elif key is 'H':
        self.hour = int(item)
      elif key is 'M':
        self.minute = int(item)
      elif key is 's':
        if item is not None:
          self.second = float(item)
      elif key is 'S':
        if item is not None:
          self.second = int(item)
      elif key is 'Z':
        if item=='Z':
          self.tz=self.tzm=0
        elif item is not None:
          (h,m)=item.split(':')
          self.tz=int(h)
          if self.tz<0:
            self.tzm=-int(m)
          else:
            self.tzm=int(m)
      else:
        raise NotImplementedError("pattern part: %%%s" % key)

  def getPat(self, fetch):
    """Try to fetch regex; if it does not exist, construct it."""
    constructors = { '%': lambda: '%'}
    #Could use dict.setdefault(), but it calls dict.__getitem__() so would
    #have to deal with second call by catching KeyError since the call will
    #fail; code below is just as clear without having to know the above 
    #fact.
    try:
      return _dict[fetch]
    except KeyError:
      if fetch in constructors:
        _dict[fetch] = constructors[fetch]()
        return _dict[fetch]
      else:
        raise NotImplementedError("fetch %s",fetch)

  def pattern(self, format):
    """Return re pattern for the format string."""
    processed_format = ''
    for whitespace in whitespace_string:
      format = format.replace(whitespace, r'\s*')
    while format.find('%') != -1:
      directive_index = format.index('%')+1
      processed_format = "%s%s%s" % (processed_format, 
                format[:directive_index-1],
                self.getPat(format[directive_index]))
      format = format[directive_index+1:]
    return "%s%s" % (processed_format, format)

  def compile(self, format):
    """Return a compiled re object for the format string."""
    return re_compile(self.pattern(format))

  def normalize(self):
    if self.tz is None:
      return
    if self.tz==0 and self.tzm==0:
      return
    if self.hour==-1:
      shouldnt1()
    if self.day==-1:
      shouldnt2()
    self.minute=self.minute-self.tzm
    self.hour=self.hour-self.tz
    self.tz=self.tzm=0
    self._cleanup()

  def _cleanup(self):
    while self.minute<0:
      self.hour=self.hour-1
      self.minute=self.minute+60
    while self.minute>59:
      self.hour=self.hour+1
      self.minute=self.minute-60
    while self.hour<0:
      self.day=self.day-1
      self.hour=self.hour+24
    while self.hour>23:
      self.day=self.day+1
      self.hour=self.hour-24
    while self.day<1:
      self.month=self.month-1
      self.day=self.day+self._dim()
    while self.day>self._dim():
      self.day=self.day-self._dim()
      self.month=self.month+1
    while self.month<1:
      self.year=self.year-1
      self.month=self.month+12
    while self.month>12:
      self.year=self.year+1
      self.month=self.month-12

  def _dim(self):
    mon = ((self.month-1)%12)+1
    if mon==2:
      if (self.year%4==0 and (self.year%100!=0 or
                              self.year%400==0)):
        return 29
      else:
        return 28
    else:
      try:
        return _months[mon]
      except:
        shouldnt('badmonth %s'%mon)

  def __cmp__(self,other):
    # assumes both are normalized
    if self.year is None:
      if other.year is None and self.hour!=-1 and other.hour!=-1:
        return self._compareTime(other)
      else:
        return None
    if self.year<other.year:
      return -1
    elif self.year>other.year:
      return 1
    else:
      # years equal
      if self.month<other.month:
        return -1
      elif self.month>other.month:
        return 1
      else:
        # months equal
        if self.day<other.day:
          return -1
        elif self.day>other.day:
          return 1
        elif self.hour==-1:
          if other.hour==-1:
            # no time, we're done
            return 0
          else:
            return None
        elif other.hour==-1:
          return None
        else:
          return self._compareTime(other)

  def _compareTime(self,other):
    if self.hour<other.hour:
      return -1
    elif self.hour>other.hour:
      return 1
    else:
      # hours equal
      if self.minute<other.minute:
        return -1
      elif self.minute>other.minute:
        return 1
      else:
        # minutes equal
        if self.second<other.second:
          return -1
        elif self.second>other.second:
          return 1
        else:
          return 0
