set -x
set -e

./manage.py migrate
./manage.py initsubjects
./manage.py inittypes
./manage.py createsuperuser
