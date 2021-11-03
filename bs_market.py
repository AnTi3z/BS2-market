#!/usr/local/www/cgi-bin/bs_market/venv/bin/python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
