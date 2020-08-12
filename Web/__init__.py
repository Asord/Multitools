from flask import Flask

flask_app = Flask(__name__)

from .index import *
from .ambibox import *