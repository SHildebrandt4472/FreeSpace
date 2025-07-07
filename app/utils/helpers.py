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
  
# Shorten a string to a maximum number of characters, adding '...' if it is shortened
def short_str(text, max_chars):
  if len(text) < max_chars:
    return text
  return text[:max_chars-3] + '...'

# Include a string if condition is true, otherwise return an empty string
# This is useful for including HTML in templates conditionally
def include_if(cond,t,f=''):
  if cond:
    return t
  return f

#
# Date Time Routines
#
def html_date(dt):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime("%Y-%m-%d")

# Convert datetime to HTML datetime format (YYYY-MM-DDTHH:MM)
def html_datetime(dt):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime('%Y-%m-%dT%H:%M')

# Format datetime to a string in the specified format
# Default format is "%d %b %y" (e.g., "01 Jan 23")
def fmt_date(dt, fmt_str="%d %b %y"):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime(fmt_str)

# Format time to a string in the specified format
# Default format is "%H:%M" (e.g., "14:30") 
def fmt_time(dt, fmt_str="%H:%M"):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime(fmt_str)

# Format datetime to a string in the specified format
# Default format is "%d %b %y %H:%M" (e.g., "01 Jan 23 14:30")
def fmt_datetime(dt, fmt_str="%d %b %y %H:%M"):
  if not isinstance(dt, datetime.datetime):
    return ''
  return dt.strftime(fmt_str)

# Format a date to a string showing how many days until that date
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

# Format a datetime to a string showing how long ago it was
def fmt_sincenow(dt, min_minutes=None):
  if not isinstance(dt, datetime.datetime):
    return ''

  try:
    diff = datetime.datetime.now() - dt
    mins = int(diff.total_seconds() / 60)
  except Exception as e:    
    return('')

  if mins < 0:                                    # just in case future date passed
    return dt.strftime("%d %b %Y, %H:%M:%S")
  if min_minutes and mins < min_minutes:
    return f"< {min_minutes} minutes ago"
  if mins == 0:
    return "< 1 minute ago"
  if mins < 120:                  # < 2 hours
    units = pluralise('minute', mins)
    return f"{mins} {units} ago"
  if mins < (2*1440):             # < 2 days
    hours = int(mins / 60)
    return f"{hours} hours ago"
  if mins < (14*1440):            # < 2 weeks
    days = int(mins / 1440)
    return f"{days} days ago"
  if mins < (60*1440):            # < 2 months
    weeks = int(mins / (7*1440))
    return f"{weeks} weeks ago"
  if mins < (730*1440):           # < 2 years
    months = int(mins / (30*1440))
    return f"{months} months ago"
  years = int(mins / (365.25*1440))
  if years < 20:
    return f"{years} years ago"
  return ''

# Generate a CSS class string for a slot based on its properties
def class_for_slot(slot):
  cls = "slot"
  cls += " time_" + slot.start_time.strftime("%H-%M")
  cls += f" dur_{slot.duration}"
  if slot.repeating:
    cls += " weekly"
  else:
    cls += " onceoff"
  return cls

# Generate a CSS class string for a booking based on its properties and the current user
def class_for_booking(slot, current_user):
  cls = "slot"
  cls += " time_" + slot.start_time.strftime("%H-%M")
  cls += f" dur_{slot.duration}"
  if slot.user_id == current_user.id:
    cls += " booked"
  elif slot.is_available():       
      if current_user.has_skills_for(slot.workspace):
        cls += " available"
      else:  
        cls += " need-skills"
  else:
    cls += " not-available"
  return cls

# Create a start time datetime object from a date and time components
def create_start_time(day,hour,min):
  return datetime.datetime.combine(day, datetime.time(hour, min, 0))



#
#  HTML Generators
#

# Generate a link to a URL with optional attributes
def link_to_url(link_text, url, attr={}):
  if not url:
    return ''
  
  html_attr = ''
  for key, value in attr.items():
    html_attr += f'{key}="{value}" '
  return f'<a href="{url}" {html_attr}>{link_text}</a>'

# Generate a link to an endpoint with optional parameters
def button_to_url(button_text, url, attr={}):
  if 'class' in attr:
    attr['class'] += ' btn btn-primary'
  else:
    attr['class'] = 'btn btn-primary'
  return link_to_url(button_text, url, attr)

# Generate a button that links to a URL
def button_to(button_text, endpoint, **endpoint_opts):
  url = url_for(endpoint, **endpoint_opts)
  return button_to_url(button_text, url)    

# Generate a form that posts to a URL with a button
def post_to_url(link_text, url, confirm_mesg="", input_class=None):  
  onclick=""
  if confirm_mesg:
    onclick = f'onclick="return customConfirm(\'{confirm_mesg}\', event)"'

  if not input_class:
    input_class = "btn btn-primary"  

  html = (f'<form class="postlink d-inline-block" action="{url}" method="post">'
          f'  <input type="submit" class="{input_class}" value="{link_text}" {onclick}>'
          f'</form>')
  return html

# Generate a form that posts to an endpoint with a button
def post_to(link_text, endpoint, confirm_mesg="", input_class=None, **endpoint_opts):
  url = url_for(endpoint, **endpoint_opts)
  return post_to_url(link_text,url, confirm_mesg=confirm_mesg, input_class=input_class)
