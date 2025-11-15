"""Entry point for the ClubHub demo web application."""

from clubhub import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
