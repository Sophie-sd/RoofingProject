#!/usr/bin/env python3
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'src'))


def main():
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.develop'),
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Is it installed and in your venv?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
