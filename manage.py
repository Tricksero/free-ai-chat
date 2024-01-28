#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from configparser import RawConfigParser

def main():
    """Run administrative tasks."""
    base_dir = Path(__file__).resolve().parent

    config = RawConfigParser()
    config.read(base_dir / 'config.ini')
    django_settings_module = config['SETTINGS']['DJANGO_SETTINGS_MODULE']

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
