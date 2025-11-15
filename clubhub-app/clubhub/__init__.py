"""Application factory for the ClubHub demo app."""

from __future__ import annotations

import os
from pathlib import Path

import click
from flask import Flask

from .models import db


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    default_db_path = instance_path / "clubhub.sqlite"

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("CLUBHUB_SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "CLUBHUB_DATABASE_URI", f"sqlite:///{default_db_path}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .views import bp as main_bp

    app.register_blueprint(main_bp)

    @app.cli.command("seed-events")
    def seed_events() -> None:
        """Populate the database with a few example events."""
        from datetime import datetime, timedelta

        from .models import Event

        if Event.query.count():
            click.echo("Database already has events; aborting.")
            return

        now = datetime.utcnow()
        sample = [
            Event(
                title="Monthly Board Meeting",
                description="Align on priorities and review upcoming programming for our members.",
                location="Community Center Room 2",
                start_time=now + timedelta(days=7),
                end_time=now + timedelta(days=7, hours=2),
                capacity=20,
                registration_deadline=now + timedelta(days=6),
            ),
            Event(
                title="Networking Social",
                description="An informal get-together to meet new members and share wins.",
                location="Rooftop Cafe",
                start_time=now + timedelta(days=14, hours=1),
                end_time=now + timedelta(days=14, hours=4),
                capacity=None,
            ),
        ]
        db.session.add_all(sample)
        db.session.commit()
        click.echo(f"Seeded {len(sample)} demo events.")

    return app
