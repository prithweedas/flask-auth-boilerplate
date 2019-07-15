#!/usr/bin/bash
export FLASK_APP=init.py
export FLASK_DEBUG=1
export FLASK_REST_SECRET='fghfytdfuyfdjhdyhgkuguyjhik'
export FLASK_REST_DB_URL='sqlite:///../site.db'
flask run