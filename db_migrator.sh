export FLASK_APP=main.py
# Run migrations
# flask db init
# flask db stamp head
flask db migrate -m "Auto Migrate"
flask db upgrade
# flask db downgrade
