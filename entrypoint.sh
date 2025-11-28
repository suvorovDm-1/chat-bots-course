#!/bin/sh
set -e

python -m bot.recreate_db_posgres
exec python -m bot