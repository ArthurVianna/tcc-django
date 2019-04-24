class setDatabases(object):
    def __init__(self):
        super(setDatabases, self).__init__()

    def getDatabases(self):
        databases = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '***',
                'USER': '***',
                'PASSWORD': '***',
                'HOST': '***',
                'PORT': '***',
            }
        }
        return databases
