import os
from icalendar import Calendar
from todoist_api_python.api import TodoistAPI
from datetime import datetime, timedelta

def read_ical_and_send_to_todoist(file_path, api_token,project_id):
  """
  Reads an iCalendar file, subtracts one day from each event, sets a fixed time 
  at 8 PM, sends each event to Todoist, and returns a list of events.

  Args:
    file_path: The path to the iCalendar file.
    api_token: Your Todoist API token.

  Returns:
    A list of events, where each event is a dictionary with the following keys:
      'summary': The event summary.
      'dtstart': The event start time (adjusted).
      'dtend': The event end time (original).
      'dtstamp': The event timestamp.
      'location': The event location.
      'description': The event description.
  """
  with open(file_path, 'r') as f:
    cal = Calendar.from_ical(f.read())

  api = TodoistAPI(api_token)
  events = []
  
  #add current date to the tag name
  tag_name = "import-" + datetime.now().strftime('%Y-%m-%d') 
  for component in cal.walk():
    if component.name == "VEVENT":
      event = {
          'summary': component.get('summary'),
          'dtstart': component.get('dtstart').dt,
          'dtend': component.get('dtend').dt,
          'dtstamp': component.get('dtstamp').dt,
          'location': component.get('location'),
          'description': component.get('description')
      }

      # Subtract one day from dtstart
      event['dtstart'] -= timedelta(days=1)

      # Set time to 8 PM
      if isinstance(event['dtstart'], datetime):
          event['dtstart'] = event['dtstart'].replace(hour=20, minute=0, second=0)
      else:
          event['dtstart'] = datetime.combine(event['dtstart'], datetime.min.time()).replace(hour=20, minute=0, second=0)

      events.append(event)

      try:
        # Create a task in Todoist with the event details
        api.add_task(
            content=event['summary'],
            due_datetime=event['dtstart'].isoformat(),
            description=f"Start: {event['dtstart']}\nEnd: {event['dtend']}\nLocation: {event['location']}\n\n{event['description']}",
            project_id=project_id,
            labels=[tag_name] 
        )
        print(f"Task '{event['summary']}' added to Todoist.")
      except Exception as e:
        print(f"Error adding task to Todoist: {e}")
        raise e
        

  return events

# Example usage
file_path = 'termine.ics'
api_token = os.environ.get('TODOIST_API_TOKEN')  # Replace with your actual API token
project_id = "6CrcwV4WRPQjCF6m"  # Replace with your actual project ID
events = read_ical_and_send_to_todoist(file_path, api_token,project_id)


for event in events:
  print(event)