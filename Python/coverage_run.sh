
# setup.py install ( https://pypi.python.org/pypi/coverage )
# pip install coverage 
# easy_install coverage 

CURRENT_DIR=$PWD
export PYTHONPATH=$CURRENT_DIR

if [ ! "$1" ]; then coverage=coverage; fi
if [ "$1" ]; then coverage=$1; fi

$coverage erase
for i in $(ls $CURRENT_DIR/*.py $CURRENT_DIR/core/*.py $CURRENT_DIR/db/*.py $CURRENT_DIR/test/*.py); do
	$coverage run --source=$CURRENT_DIR --append $i
done
$coverage report --show-missing
