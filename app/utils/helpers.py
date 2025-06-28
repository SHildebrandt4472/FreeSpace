#
# HTML Helper functions
#

import datetime
from flask import url_for

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

def html_datetime(dt):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime('%Y-%m-%dT%H:%M')

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

def class_for_slot(slot):
  cls = "slot"
  cls += " time_" + slot.start_time.strftime("%H-%M")
  cls += f" dur_{slot.duration}"
  if slot.user_id:
    cls += " not_available"
  else:
    cls += " available"
  return cls

def create_start_time(day,hour,min):
  return datetime.datetime.combine(day, datetime.time(hour, min, 0))

#
#  HTML Generators
#
def link_to_url(link_text, url, attr={}):
  if not url:
    return ''
  
  html_attr = ''
  for key, value in attr.items():
    html_attr += f'{key}="{value}" '
  return f'<a href="{url}" {html_attr}>{link_text}</a>'

def button_to_url(button_text, url, attr={}):
  if 'class' in attr:
    attr['class'] += ' btn btn-primary'
  else:
    attr['class'] = 'btn btn-primary'
  return link_to_url(button_text, url, attr)

def post_to_url(link_text, url, confirm_mesg=""):  
  onclick=""
  if confirm_mesg:
    onclick = f'onclick="return confirm(\'{confirm_mesg}\')"'

  html = (f'<form class="postlink" action="{url}" method="post">'
          f'  <input type="submit" class="btn btn-primary" value="{link_text}" {onclick}>'
          f'</form>')
  return html

def post_to(link_text, endpoint, confirm_mesg="", **endpoint_opts):
  url = url_for(endpoint, **endpoint_opts)
  return post_to_url(link_text,url, confirm_mesg=confirm_mesg)
