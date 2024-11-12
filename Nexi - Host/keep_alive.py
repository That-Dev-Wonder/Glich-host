from flask import Flask
from threading import Thread
import logging
import os

# Disable Flask's default logging to reduce console spam
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

def run():
    port = int(os.getenv('PORT', 8000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False
    )

def keep_alive():
    server = Thread(target=run)
    server.daemon = False
    server.start()