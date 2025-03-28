#!/bin/bash
# Script pour démarrer le serveur Flask sur Koyeb
gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120