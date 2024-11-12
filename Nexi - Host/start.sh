#!/bin/bash
gunicorn keep_alive:app &
python bot.py