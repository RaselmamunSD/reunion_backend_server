#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reunion_backend_server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    
    # Add IPv6 support for runserver command
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        if len(sys.argv) == 2:  # If no host:port specified
            sys.argv.append('[::]:8000')  # Listen on all interfaces, IPv4 and IPv6
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main() 