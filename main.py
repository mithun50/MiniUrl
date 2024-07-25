# run.py
import threading
import setup_database
from bot import start_bot
from server import start_flask
from add_admin import add_admin
import os

def run_all():
    # Set up the database
    setup_database.setup_database()
    username = os.getenv("Usr")
    password = os.getenv('Pass')
    add_admin(username=username, password=password)

    
    # Start both bot and Flask server in separate threads
    threading.Thread(target=start_bot).start()
    threading.Thread(target=start_flask).start()

if __name__ == '__main__':
    run_all()

