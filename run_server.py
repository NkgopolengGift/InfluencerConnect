import os
import sys
import logging
from django.core.management import execute_from_command_line

# Set up logging
logging.basicConfig(filename="server.log", level=logging.DEBUG)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InfluencerConnect.settings')
    try:
        execute_from_command_line(sys.argv + ['runserver'])
    except Exception as e:
        logging.exception("Exception occurred while running the server")
        sys.exit(1)
