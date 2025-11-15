"""HTTP handlers for the ClubHub demo app."""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash

from .models import Event, Registration, db

bp = Blueprint("main", __name__)

_DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, _DATETIME_FORMAT)
    except ValueError:
        return None


@bp.route("/")
def index():
    events = Event.query.order_by(Event.start_time.asc()).all()
    return render_template("index.html", events=events)


@bp.route("/events/new", methods=["GET", "POST"])
def create_event():
    errors: list[str] = []
    form_data = request.form or None

    if request.method == "POST":
        title = (form_data.get("title") or "").strip()
        description = (form_data.get("description") or "").strip()
        location = (form_data.get("location") or "").strip()
        start_time = _parse_datetime(form_data.get("start_time"))
        end_time = _parse_datetime(form_data.get("end_time"))
        registration_deadline = _parse_datetime(form_data.get("registration_deadline"))

        capacity_raw = form_data.get("capacity")
        capacity = None
        if capacity_raw:
            try:
                capacity = max(int(capacity_raw), 0)
            except ValueError:
                errors.append("Capacity must be a whole number.")

        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not location:
            errors.append("Location is required.")
        if not start_time or not end_time:
            errors.append("Start and end times are required.")
        elif end_time <= start_time:
            errors.append("End time must be after the start time.")
        if registration_deadline and start_time and registration_deadline > start_time:
            errors.append("Registration deadline must be before the event starts.")

        if not errors:
            event = Event(
                title=title,
                description=description,
                location=location,
                start_time=start_time,
                end_time=end_time,
                capacity=capacity,
                registration_deadline=registration_deadline,
            )
            db.session.add(event)
            db.session.commit()
            flash("Event created successfully!", "success")
            return redirect(url_for("main.event_detail", event_id=event.id))
        flash("Please fix the issues below.", "error")

    return render_template("events/new.html", errors=errors)


@bp.route("/events/<int:event_id>")
def event_detail(event_id: int):
    event = Event.query.get_or_404(event_id)
    attendees = event.registrations.order_by(Registration.created_at.asc()).all()
    return render_template("events/detail.html", event=event, attendees=attendees)


@bp.route("/events/<int:event_id>/register", methods=["POST"])
def register(event_id: int):
    event = Event.query.get_or_404(event_id)
    name = (request.form.get("attendee_name") or "").strip()
    email = (request.form.get("attendee_email") or "").strip()

    if not name or not email:
        flash("Name and email are required to register.", "error")
        return redirect(url_for("main.event_detail", event_id=event.id))

    if event.registration_deadline and datetime.utcnow() > event.registration_deadline:
        flash("Registration deadline has passed.", "error")
        return redirect(url_for("main.event_detail", event_id=event.id))

    if event.is_full:
        flash("This event is full.", "error")
        return redirect(url_for("main.event_detail", event_id=event.id))

    registration = Registration(attendee_name=name, attendee_email=email, event=event)
    db.session.add(registration)
    db.session.commit()
    flash("You have been registered!", "success")
    return redirect(url_for("main.event_detail", event_id=event.id))


@bp.route("/api/events")
def api_events():
    events = Event.query.order_by(Event.start_time.asc()).all()
    payload = [
        {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "location": event.location,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat(),
            "capacity": event.capacity,
            "spots_remaining": event.spots_remaining,
        }
        for event in events
    ]
    return jsonify(payload)
