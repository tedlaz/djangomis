#!/bin/bash
gunicorn --bind 0.0.0.0:8008 djangomis.wsgi
