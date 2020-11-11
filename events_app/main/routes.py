"""Import packages and modules."""
import os
import requests
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    jsonify,
)
from datetime import date, datetime
from pprint import PrettyPrinter
from events_app.main.utils import get_holiday_data
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import db

main = Blueprint("main", __name__)

##########################################
#            App setup                   #
##########################################

# Define global variables (stored here for now)

# This initializes our PrettyPrinter object:

pp = PrettyPrinter(indent=4)

today = date.today()
# Now, let's just get the month as a number:
month = today.strftime("%m")
# Now, let's get the current year:
year = today.strftime("%Y")
# I also want to know the name of the month for later:
month_name = today.strftime("%B")


##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    """
    Return template for home.

    This is the single HTML page we need to serve from
    our back end.
    """
    return render_template("index.html")


@main.route("/events")
def show_events():
    """
    Return all events from database.

    Our front end will use this to display these
    to users.
    """
    events = Event.query.all()
    data = [
        {
            "name": event.title,
            "description": event.description,
            "date": event.date.strftime("%M-%d-%Y"),
            "time": event.time.strftime("%H:%M"),
        }
        for event in events
    ]
    return jsonify({"data": data}), 200


@main.route("/add-event", methods=["POST"])
def add_event():
    """Add event to Event table."""
    try:
        new_event_title = request.form.get("title")
        new_event_description = request.form.get("description")
        new_event_date = datetime.strptime(
            request.form.get("date"), "%m-%d-%Y"
        )
        new_event_time = datetime.strptime(request.form.get("time"), "%H:%M")

        event = Event(
            title=new_event_title,
            description=new_event_description,
            date=new_event_date,
            time=new_event_time,
            guests=[],
        )

        db.session.add(event)
        db.session.commit()
        return (
            jsonify({"msg": "Event added successfully", "data": event}),
            200,
        )
    except ValueError:
        return jsonify(
            {
                "msg": """
                Something went wrong, please verify that you've entered
                everything in the correct format and try again.
                """
            }
        )


@main.route("/delete-event/<event_id>", methods=["POST"])
def delete_event(event_id):
    """
    Delete event.

    Delete event after the date it occurs automatically.
    """
    event = Event.query.filter_by(id=event_id).first()
    db.session.delete(event)
    db.session.commit()
    return jsonify({"msg": "Successfully deleted."}), 200


@main.route("/edit-event/<event_id>", methods=["POST"])
def edit_event(event_id):
    """Edit events."""
    event = Event.query.filter_by(id=event_id).first()

    new_event_title = request.form.get("title")
    new_event_description = request.form.get("description")
    new_event_date = datetime.strptime(request.form.get("date"), "%m-%d-%Y")
    new_event_time = datetime.strptime(request.form.get("time"), "%H:%M")

    event.title = new_event_title
    event.description = new_event_description
    event.date = new_event_date
    event.time = new_event_time

    db.session.commit()
    return jsonify({"msg": "Updated successfully.", "data": event}), 200


@main.route("/holidays")
def about_page():
    """Show user event information."""
    url = "https://calendarific.com/api/v2/holidays"

    params = {
        "api_key": os.getenv("API_KEY"),
        "country": "US",
        "year": year,
        "month": month,
    }

    result_json = requests.get(url, params=params).json()
    # You can use pp.pprint() to print out your result -
    # This will help you know how to access different items if you get stuck
    # pp.pprint(result_json)

    # Call get_holiday_data to return our list item

    holidays = get_holiday_data(result_json)

    return jsonify({"data": {"holidays": holidays, "month": month_name}}), 200


@main.route("/guests", methods=["GET", "POST"])
def show_guests():
    """
    Show guests that have RSVP'd.

    Add guests to RSVP list if method is POST.
    """
    events = Event.query.all()
    data = [
        {
            "name": event.title,
            "description": event.description,
            "date": event.date.strftime("%M-%d-%Y"),
            "time": event.time.strftime("%H:%M"),
        }
        for event in events
    ]
    if request.method == "GET":
        return jsonify({"data": data}), 200
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plus_one = request.form.get("plus-one")
        phone = request.form.get("phone")
        event_id = request.form.get("event_id")

        event = Event.query.filter_by(id=event_id).first()

        guest = Guest(
            name=name,
            email=email,
            plus_one=plus_one,
            phone=phone,
            events_attending=[],
        )

        event.guests.append(guest)

        print(f"Event guests: {event.guests}")

        db.session.add(guest)
        db.session.commit()

        return jsonify({"msg": "new guest added.", "data": data})


@main.route("/rsvp")
def rsvp_guest():
    """Show form for guests to RSVP for events."""
    events = Event.query.all()
    data = [
        {
            "name": event.title,
            "description": event.description,
            "date": event.date.strftime("%M-%d-%Y"),
            "time": event.time.strftime("%H:%M"),
        }
        for event in events
    ]
    return jsonify({"data": data}), 200
