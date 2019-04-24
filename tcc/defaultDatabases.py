class setDatabases(object):
    def __init__(self):
        super(setDatabases, self).__init__()

    def getDatabases(self):
        databases = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'tcc',
                'USER': 'arthur',
                'PASSWORD': 'abc123',
                'HOST': '192.168.99.100',
                'PORT': '3306',
            }
        }
        return databases