import os
import sys
import random
import atexit
import signal
import pickle
import json
from subprocess import call
from models.models import Joueur, Tournoi, Tour, Match
from views.vues import Ihm
from tinydb import TinyDB, where, Query

# sys.path.append("/Users/hhmbp/Documents/OC/P4/p4C/models")
# sys.path.append("/Users/hhmbp/Documents/OC/P4/p4C/views")
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
print(currentdir)
print(parentdir)
sys.path.append(parentdir)
jrap = Joueur()
trs = Tour()
trns = Tournoi()
mtchs = Match()
db = TinyDB('../database.json')
jdb = TinyDB('../joueurs.json')
sdb = TinyDB('../savedb.json')
# db = TinyDB('bdd/database.json')
joueurs_table = jdb.table('joueurs')
tournois_table = db.table('tournois')
match_table = db.table('match')
tour_table = db.table('tour')

# print(*tournois_table.all())
