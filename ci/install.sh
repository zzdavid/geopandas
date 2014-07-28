#!/bin/bash

PANDAS_WHEELS=http://pandas.pydata.org/pandas-build/dev/wheels
ASTROPY_WHEELS=http://wheels2.astropy.org

pip install -I --use-wheel --find-links=$PANDAS_WHEELS/$TRAVIS_PYTHON_VERSION --allow-external --allow-insecure -r requirements.txt
pip install -I --use-wheel --find-links=$PANDAS_WHEELS/$TRAVIS_PYTHON_VERSION --allow-external --allow-insecure -r requirements.test.txt
if [[ $TRAVIS_PYTHON_VERSION == '2.6' ]]; then
    pip install -r .requirements-2.6.txt --use-mirrors
fi

if [[ $PANDAS_VERSION == 'master' ]]; then
    git clone git://github.com/pydata/pandas.git
    cd pandas
    git checkout $PANDAS_VERSION
    python setup.py install
else
    pip install -I --use-wheel --find-links=$ASTROPY_WHEELS --allow-external --allow-insecure pandas==$PANDAS_VERSION
fi
