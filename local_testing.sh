#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d ".venv" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .venv/bin/activate
export ENV=testing
export FLASK_APP=main.py
# Run migrations
flask db init
flask db stamp head
flask db migrate -m "Temporary migration message"
flask db upgrade

# pytest --verbose --disable-warnings -s
deactivate
