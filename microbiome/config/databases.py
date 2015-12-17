import os

from unipath import Path

# expect at ~/source/microbiome/etc/default.cnf
# etc folder is not in the git repo
PATH = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(2).child('etc')

if not os.path.exists(PATH):
    raise TypeError('Path to database credentials at \'{}\' does not exist'.format(PATH))

with open(os.path.join(PATH, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

PRODUCTION_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(PATH, 'default.cnf'),
        },
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(PATH, 'lab_api.cnf'),
        },
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
}

TRAVIS_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'database': 'mb',
            'user': 'travis',
            'default-character-set': 'utf8',
            'init_command': 'SET storage_engine=INNODB',
        },
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'database': 'lab',
            'user': 'travis',
            'default-character-set': 'utf8',
            'init_command': 'SET storage_engine=INNODB',
        },
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
}
