from threading import Thread
from scheduler import start_scheduler
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome!"


if __name__ == "__main__":
    # Run scheduler to fetch papers in a separate thread
    scheduler_thread = Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

    app.run(debug=True, use_reloader=False)
