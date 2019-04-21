#runScript in shell
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcc.settings")

import django
django.setup()

# your imports, e.g. Django models
from tccStudentRegistration.models import *
from tccStudentRegistration.importCSV import *