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
export ENV=development
export FLASK_APP=main.py
# Run migrations
flask db migrate -m "Database migration"
flask db upgrade

python main.py
deactivate
