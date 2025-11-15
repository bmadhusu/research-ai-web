"""Database models for events and registrations."""

from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    registration_deadline = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    registrations = db.relationship(
        "Registration",
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    @property
    def spots_remaining(self) -> int | None:
        if self.capacity is None:
            return None
        return max(self.capacity - self.registrations.count(), 0)

    @property
    def is_full(self) -> bool:
        remaining = self.spots_remaining
        return remaining is not None and remaining <= 0

    def __repr__(self) -> str:  # pragma: no cover - repr helper
        return f"<Event {self.title!r} at {self.start_time:%Y-%m-%d}>"


class Registration(db.Model):
    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    attendee_name = db.Column(db.String(120), nullable=False)
    attendee_email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    event = db.relationship("Event", back_populates="registrations")

    def __repr__(self) -> str:  # pragma: no cover - repr helper
        return f"<Registration {self.attendee_email!r} for event {self.event_id}>"
