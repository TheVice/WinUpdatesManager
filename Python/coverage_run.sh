
# setup.py install ( https://pypi.python.org/pypi/coverage )
# pip install coverage 
# easy_install coverage 

CURRENT_DIR=$PWD
export PYTHONPATH=$CURRENT_DIR

coverage erase
for i in $(ls $CURRENT_DIR/*.py $CURRENT_DIR/core/*.py $CURRENT_DIR/db/*.py $CURRENT_DIR/test/*.py); do
	coverage run -a $i
done
coverage report -m
