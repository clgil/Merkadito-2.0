import sys
import os

# Path al virtualenv en Hostinger (ajustar según configuración)
INTERP = os.path.expanduser("/home/u123456789/virtualenvs/merkadito/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Agregar el directorio del proyecto al path
sys.path.append(os.getcwd())
os.chdir(os.path.dirname(__file__))

from merkadito.wsgi import application
