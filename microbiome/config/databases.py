import os

from unipath import Path

try:
    # expect at ~/source/microbiome/etc/default.cnf
    # etc folder is not in the git repo
    PATH = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(2).child('etc')
    if not os.path.exists(PATH):
        raise TypeError('Path to database credentials at \'{}\' does not exist'.format(PATH))
    with open(os.path.join(PATH, 'secret_key.txt')) as f:
        PRODUCTION_SECRET_KEY = f.read().strip()
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
except TypeError:
    PRODUCTION_MYSQL = None
    PRODUCTION_SECRET_KEY = None
    print('Path to production database credentials does not exist')

TRAVIS_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mb',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mb_lab',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
}

TEST_HOSTS_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mb',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mb_lab',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
}
