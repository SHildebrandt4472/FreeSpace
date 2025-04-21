#
# HTML Helper functions
#

import datetime

#
# General Text Formatting
#


def pluralise(word, cnt, suffix="s"):
  n = int(cnt)
  if n == 1 or n == -1:
    return(word)
  else:
    return(word+suffix)

#
# Date Time Routines
#

def html_date(dt):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime("%Y-%m-%d")

def fmt_date(dt):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime("%d %b %y")

def fmt_date_daysuntil(date):
  if not isinstance(date, datetime.datetime):
    return ''
  
  try:
    diff = date.date() - datetime.date.today()
    days = int(diff.total_seconds() / (60*60*24))
  except Exception as e:    
    return('')   
  
  days_str = pluralise('day', days)

  if days < -1: 
    return f"{-days} {days_str} ago"
  if days == -1:
    return 'Yesterday'
  if days == 0:
    return 'Today'
  if days == 1:
    return 'Tomorrow'
  
  return f"{days} {days_str}"


