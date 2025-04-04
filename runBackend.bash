#!/usr/bin/env bash
cd backend && uvicorn main:app --host 0.0.0.0 --port 8080 --reload
#ouvrir le terminal taper:  ./runBackend.bash
#ouvrir le browser taper localhost:8080/ (suivi du path que vous voulez voir)
#terminer le programme sur le terminal avec ctrl c