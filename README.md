# Addok-geozones

Helpers to run a Geozones dedicated Addok instance.


## Install

If you are using macOS and geos installed via homebrew,
start by installing Shapely with:

    pip install Shapely==1.5.17 --no-binary :all:


Install addok, addok-trigrams and addok-geozones (this repository):

    pip install addok
    pip install addok-trigrams
    pip install git+https://github.com/addok/addok-geozones


Copy the sample local config:

    cp local.py.sample somewhere/local.py

It should work as is, but you can have a look at the
[addok configuration](http://addok.readthedocs.io/en/latest/config/)
to adapt it to your needs.

This plugin adds two configuration keys that needs more consideration:

- GEOZONES_LEVELS will define which levels are imported
- GEOZONES_MAX_IMPORTANCE help computing the importance of the
  documents


## Importing

Get the zones from https://www.data.gouv.fr/fr/datasets/geozones/
Then:

    addok batch path/to/zones.msgpack --config=local.py
