#!/bin/bash

ASTROPY_WHEELS=http://wheels.astropy.org
ASTROPY_WHEELS2=http://wheels2.astropy.org

PIP_OPTIONS="-I --use-wheel --find-links=$ASTROPY_WHEELS --find-links=$ASTROPY_WHEELS2 --allow-external --allow-insecure"

pip install $PIP_OPTIONS -r requirements.txt
pip install $PIP_OPTIONS -r requirements.test.txt
if [[ $TRAVIS_PYTHON_VERSION == '2.6' ]]; then
    pip install $PIP_OPTIONS -r .requirements-2.6.txt --use-mirrors
fi

if [[ $PANDAS_VERSION == 'master' ]]; then
    pip install git+git://github.com/pydata/pandas.git
else
    pip install $PIP_OPTIONS pandas==$PANDAS_VERSION
fi
