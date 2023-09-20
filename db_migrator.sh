export FLASK_APP=main.py
# Run migrations
# flask db stamp head
# flask db migrate -m "added quantity in product table"
flask db upgrade
# flask db downgrade
