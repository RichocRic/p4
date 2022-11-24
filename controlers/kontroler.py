"""Controleur du programme d'échecs."""
import os
import sys
import random
import atexit
import json
import uuid
from subprocess import call
from models.models import Joueur, Tournoi, Tour, Match
from views.vues import Ihm
from tinydb import TinyDB, where

sys.path.append("/Users/hhmbp/Documents/OC/P4/p4C/models")
sys.path.append("/Users/hhmbp/Documents/OC/P4/p4C/views")
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)

# sys.path.append(parentdir)
jrap = Joueur()
trs = Tour()
trns = Tournoi()
mtchs = Match()
# db = TinyDB('../database.json')
# jdb = TinyDB('../joueurs.json')
# sdb = TinyDB('../savedb.json')

jdb = TinyDB('../joueurs.json')
db = TinyDB('../database.json')
sdb = TinyDB('../savedb.json')
# db = TinyDB('bdd/database.json')
joueurs_table = jdb.table('joueurs')
tournois_table = db.table('tournois')
match_table = db.table('match')
tour_table = db.table('tour')

sdbjoueurs_table = sdb.table('sdbjoueurs')
sdbtournois_table = sdb.table('sdbtournois')
sdbmatch_table = sdb.table('sdbmatch')
sdbtour_table = sdb.table('sdbtour')
# logging.basicConfig(filename='logs/journal.log', encoding='utf-8', level=logging.DEBUG)
ID_TOURNOI_ENCOURS = ""
lstIdParticipant = ""
id_Tour_transmettre = ""
sauvTour = "blackout.json"
selctionmem = ""
djoueur = {}
infoSaisie = []
rmj1 = ""
rmj2 = ""
id_j1 = ""
id_j2 = ""


# signal.signal(signal.SIGHUP, handler)


class Maincontroller:
    """Creation de la classe controler."""

    def __init__(self):
        """Constructeur."""

    @staticmethod
    def associer(clef, choix):
        """Associations."""
        donnees = []
        if choix == 1:
            donnees.append(Ihm.ltourn[0])
        elif choix == 2:
            donnees.append(Ihm.ljouee[0])
        elif choix == 4:
            donnees.append(ID_TOURNOI_ENCOURS)
            donnees.append(lstIdParticipant)
            donnees.append(rmj1)
            donnees.append(rmj2)
            donnees.append(id_j1)
            donnees.append(id_j2)
            donnees.append(Maincontroller.id_tourreprise(ID_TOURNOI_ENCOURS))

        # print(donnees)
        tail = len(donnees)
        # print(tail)
        id_tour = Maincontroller.id_tourprendre(ID_TOURNOI_ENCOURS)
        # print(id_tour)
        round_tour = Maincontroller.id_tourreprise(ID_TOURNOI_ENCOURS)
        # print(round_tour)
        jrs = Maincontroller.id_tour_lstjoueurs(ID_TOURNOI_ENCOURS)
        # print(jrs)
        dico = {}
        for i in range(0, tail):
            for x in donnees:
                dico[clef[i]] = donnees[i]
            with open("savedb.json", "w") as outfile:
                json.dump(dico, outfile)
        Joueur.message("SAUVEGARDE OK")
        print(dico)

    @staticmethod
    def handler():
        """Detect terminal closure and save data."""
        Joueur.message("SAUVEGARDE EN COURS...")
        print("la selection vaut:", selctionmem)
        if selctionmem == 1:
            print("Tournois")
            clef = ["nom du tournois", "lieu du tournois", "date du tournois", "nombre de tour",
                    "contrôle de temps", "id des joueurs", "nombre de participants", "la description du tournois"]
            Maincontroller.associer(clef, selctionmem)

        elif selctionmem == 2:
            print("CHOIX 2")
            case = {"ligne": selctionmem}
            Joueur.message("SAUVEGARDE EN COURS...")
            clef = ["Nom du joueur", "Prénom du joueur", "Âge du joueur", "Sexe du joueur", "Classement du joueur"]
            Maincontroller.associer(clef, selctionmem)

        elif selctionmem == 4:
            print("CHOIX 4")
            Joueur.message("SAUVEGARDE EN COURS...")
            # clef = ["ID TOURNOIS EN COURS", "ID TOUR", "NOMBRE DE TOUR", "numMatches"]
            clef = ["ID TOURNOIS EN COURS", "LISTPARTICIPANT", "RESULTAT MATCH J1", "RESULTAT MATCH J2", "ID JOUEUR1",
                    "ID JOUEUR2", "TOUR N°"]
            Maincontroller.associer(clef, selctionmem)

    @staticmethod
    def reprise():
        """Reprise saisie tournois joueurs."""
        clefj = ["Nom du joueur", "Prénom du joueur", "Âge du joueur", "Sexe du joueur", "Classement du joueur"]

        cleft = ["nom du tournois", "lieu du tournois", "date du tournois", "nombre de tour",
                 "contrôle de temps", "nombre de participants", "la description du tournois"]

        clefm = ["ID TOURNOIS EN COURS", "LISTPARTICIPANT", "RESULTAT MATCH J1", "RESULTAT MATCH J2", "ID JOUEUR1",
                 "ID JOUEUR2", "TOUR N°"]

        file_size = os.stat(r'/Users/hhmbp/Documents/OC/P4/P4C/savedb.json')
        dicoEntb = []
        # print("la taille est de :", file_size.st_size)
        if file_size.st_size == 0:
            print("AUCUNE SAUVEGARDE ACTUELLEMENT")
        else:
            print("Sauvegarde trouvée.")
            # fich = '/Users/hhmbp/Documents/OC/P4/P4C/savedb.json'
            fich = sdb
            with open(fich, 'r', encoding='utf-8', newline='') as f:
                dico = json.load(f)
                # print(dico[0])
                # print(type(dico))
                print("Taille dico: ", len(dico.items()))
                tclefj = len(clefj)
                tcleft = len(cleft)
                tclefm = len(clefm)
                tdico = len(dico.items())
                sauv = 0
                for a in dico.values():
                    dicoEntb.append(a)

                for c, v in dico.items():
                    if c == "Nom du joueur":
                        sauv = 2
                        # print("2")
                        break
                    elif c == "nom du tournois":
                        sauv = 1
                        # print("1")
                        break
                    elif c == "ID TOURNOIS EN COURS":
                        sauv = 4
                        # print("4")
                        break
                    else:
                        print("problème de récupération de données")
                        break

            print("==>", sauv)
            if sauv == 2:
                # print("Long dico: ", tdico)
                # print("Long clef: ", tclefj)

                for i in range(tdico, tclefj):
                    # print("I vaut: ", i)
                    saisi = input("saisir : " + clefj[i])
                    dicoEntb.append(saisi)
                njoueur = Joueur()
                njoueur.creation_joueur(dicoEntb)
                njoueur.inserer_bdd('joueurs')

            elif sauv == 1:
                # print("Long dico: ", tdico)
                # print("Long clef: ", tcleft)
                for j in range(tdico, tcleft):
                    # print("J vaut: ", j)
                    saisieT = input("saisir : " + cleft[j])
                    dicoEntb.append(saisieT)
                ntournoi = Tournoi()
                ntournoi.creation_tournoi(dicoEntb)
                ntournoi.inserer_bdd('tournoi')
            elif sauv == 4:
                '''Récupération de lid tournoi en cours '''
                ID_TOURNOI_ENCOURS = dico.values()
                print(dico.values())
                '''Récupération du round en cours '''

    @staticmethod
    def selectionJoueurs():
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        lstjoueurs = Ihm.saisir_joueur()
        recupid = []
        for entry in tournois_table.all():
            # if lstjoueurs[] == doc_id:
            recupid.append(entry['Identifiant du joueur'])

    @staticmethod
    def idtournoiencours():
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        tourn_ids = []
        for entry in tournois_table.all():
            if entry['id du tournois']:
                tourn_ids.append(entry['id du tournois'])
                global ID_TOURNOI_ENCOURS
        ID_TOURNOI_ENCOURS = entry['id du tournois']
        print("l'id du tournois vaut:", ID_TOURNOI_ENCOURS)
        # print("Le tournois vaut:", tournois_table.all())
        # nbrTour = len(tour_ids)
        return tourn_ids

    @staticmethod
    def id_tourprendre(ID_TOURNOI_COUR):
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        tour_ids = []
        for entry in tour_table.all():
            if entry['id tournois'] == ID_TOURNOI_COUR:
                tour_ids.append(entry['id du tour'])
        # nbrTour = len(tour_ids)
        return tour_ids

    @staticmethod
    def id_tourreprise(ID_TOURNOI_COUR):
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        tour_ids = []
        for entry in tour_table.all():
            if entry['id tournois'] == ID_TOURNOI_COUR:
                tour_ids.append(entry['id du tour'])
        nbrTour = len(tour_ids)
        return nbrTour

    @staticmethod
    def id_tour_lstjoueurs(ID_TOURNOI_COUR):
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        lst_jrs = []
        for entry in tour_table.all():
            if entry['id tournois'] == ID_TOURNOI_COUR:
                lst_jrs.append(entry['liste des matches'])
        # nbrTour = len(tour_ids)
        return lst_jrs

    # str_jrs = ' '.join(str(elem) for elem in jrs)
    # str_jrs = jrs[0]
    # Ajouter la liste des joueurs
    # print("N° tour: ", round_tour)
    # print("Tournois id: ", ID_TOURNOI_ENCOURS)
    # print("JoueursLst: ", str_jrs)
    # print("ID tour: ", id_tour)
    '''appeller la méthode saisir '''

    # Controlertournoi.saisir_match(str_jrs, round_tour, "31e57338-4946-11ed-9d14-acde48001122")

    # print("Long clef: ", tcleft)

    @staticmethod
    def demarrer():
        """Lancement du menu/menu launcher."""
        ctrl = Controleurmenu('n')
        ctrl.gestionchoix()


class Controleurjoueurs:
    """Controleur du menu joueur."""

    def __init__(self, nom):
        """Constructeur."""
        self.nom = nom

    @staticmethod
    def creation_joueurs():
        """Création dynamique de 8 joueurs comme demandé."""
        joueur = []
        nbrjoueur = int(input('Sasir, le Nombre de joueur(s) à inserrer '))
        for i in range(nbrjoueur):
            print('=========================')
            print('Instance Joueur N°:', [i])
            print('=========================\n')
            joueur.append(Joueur())
            joueur[i] = Joueur()
            joueur[i].creation_joueur(Ihm.creat_joueur())
            joueur[i].inserer_bdd('joueurs')


class Controleurrappport:
    """Controleur de Gestion des rapports."""

    def __init__(self, nom):
        """Constructeur."""
        self.nom = nom

    @staticmethod
    def triejoueur(valeur):
        """TrierDesJoueurs."""
        doc_ids = []
        for entry in joueurs_table.all():
            doc_ids.append([entry['Identifiant du joueur'],
                            entry['Nom du joueur'],
                            entry['Prénom du joueur'],
                            entry['Âge du joueur'],
                            entry['Sexe du joueur'],
                            entry['Classement du joueur'],
                            entry['Score du joueur']
                            ])
        if valeur == "c":
            clssmnt = sorted(joueurs_table.all(), key=lambda x: x['Classement du joueur'], reverse=True)
        elif valeur == "s":
            clssmnt = sorted(joueurs_table.all(), key=lambda x: x['Score du joueur'], reverse=True)
        else:
            print('demande non comprise')
            clssmnt = sorted(joueurs_table.all(), key=lambda x: x['Identifiant du joueur'], reverse=True)
        return clssmnt


class Controlermenugestion:
    """Manage displaying and lifecycle."""

    @staticmethod
    def afficher_msg(msg):
        """Personnaliser les msg."""
        print(msg)

    @staticmethod
    def effacer_ecran():
        """Détection des O.S."""
        _ = call('clear' if os.name == 'posix' else 'cls')
        Controlermenugestion.effacer_ecran()

    @staticmethod
    def sortir():
        """Sortie du menu."""
        sys.exit()


class Controlertournoi:
    """Classe tournois controleur."""

    ctrl3 = Controleurjoueurs('T3')

    # global ID_TOURNOI_ENCOURS

    def __init__(self, nom):
        """Constructeur."""
        self.nom = nom

    @staticmethod
    def maj(idtour):
        """MAJ du tournois."""
        df = trns.donner_temps('j')
        hf = trns.donner_temps('h')
        print(hf)
        print(df)
        tour_table.update({'heure de fin': hf}, where('id du tour') == idtour)
        tour_table.update({'date de fin': df}, where('id du tour') == idtour)

    @staticmethod
    def selectionparticipant(nbr_joueurs):
        """Sélection aléatoire de joueurs."""
        joueurs_ids = []
        for valeur in joueurs_table.all():
            joueurs_ids.append(valeur["Identifiant du joueur"])
        selectionparticipant = random.sample(joueurs_ids, int(nbr_joueurs))
        return selectionparticipant

    @staticmethod
    def lstidtournois(table):
        """Retourne la liste des id Tournois. ou id Tour."""
        doc_ids = []
        if table == tournois_table:
            for valeur in tournois_table.all():
                if not valeur['id des joueurs']:
                    doc_ids.append(valeur["id du tournois"])
        elif table == tour_table:
            doc_ids = list(map(lambda x: x["id du tour"], table))
        return doc_ids

    @staticmethod
    def id_tour(ID_TOURNOI_COUR):
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        tour_ids = []
        for entry in tour_table.all():
            if entry['id tournois'] == ID_TOURNOI_COUR:
                tour_ids.append(entry['id du tour'])
        # nbrTour = len(tour_ids)
        return tour_ids

    @staticmethod
    def donnerLstMatchs():
        """Liste des matchs dans la table tour."""
        lstmatchs = []
        idtourn = Maincontroller.idtournoiencours()
        print('id Tournois en cours', idtourn)
        derniertour = Controlertournoi.id_tour(idtourn[0])
        # print("<==TOTO DERNIER==>",derniertour)
        # derniertour = derniertour[-1]

        for entry in tour_table.all():
            # print("<==TOTO DERNIER==>", derniertour)
            print("<==ENTRY DERNIER==>", entry['id du tour'])
            if entry['id du tour'] == derniertour[-1]:
                # lstmatchs.append(entry['liste des matches'])
                lstmatchs.append(entry['liste des matches'])
                print('id du dernier tour:', derniertour[-1])
                global id_Tour_transmettre
                id_Tour_transmettre = derniertour[-1]
        print(lstmatchs)
        return lstmatchs

    @staticmethod
    def matchmanquant():
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        idtourn = Maincontroller.idtournoiencours()
        # print('id Tournois en cours',idtourn)
        derniertour = Controlertournoi.id_tour(idtourn[0])
        # derniertour = derniertour[-1]
        print('MatchsManquant id des tours:', derniertour[-1])
        nbrmatchs = []
        # list(map(lambda x: x["id tour"], match_table.all()))
        tlistidtour = len(derniertour)
        print('taille de la liste:', tlistidtour)
        for entry in match_table.all():
            for i in range(0, tlistidtour):
                if entry['id tour'] == derniertour[i]:
                    nbrmatchs.append(entry['id tour'])
        matchmanquant = nbrmatchs.count(derniertour[-1])
        print("Nombre de Match trouvé pour le dernier tour:", matchmanquant)
        return matchmanquant

    @staticmethod
    def acompleter():
        """Reprise tournois."""
        id_tournois = Maincontroller.idtournoiencours()
        id_tour = Controlertournoi.id_tour(id_tournois[0])
        print("id tour dans à completer: ", id_tour)
        lstmatch = Controlertournoi.donnerLstMatchs()
        trouver = Controlertournoi.matchmanquant()
        print("LISTE DES MATCHES BRUTES AVANT CORRECTION", lstmatch)
        for j in range(1, trouver):
            del lstmatch[0][0]
            print("LISTE DES MATCHES BRUTES APRES CORRECTION", lstmatch[0][0])
        # del lstmatch[0][0]
        # del lstmatch[0][0]
        print("LISTE DES MATCHES BRUTES APRES CORRECTION", lstmatch[0][0])
        nbrmanquant = 4 - trouver
        print("RESTE à faire:", nbrmanquant)
        elms = []
        elms.append(nbrmanquant)
        elms.append(id_tournois)
        elms.append(id_tour[-1])
        elms.append(lstmatch)
        # print(elms[3][0][1][0])
        # elemnt = elms[3][0]
        # elms = elms[3][0]
        # print(elemnt)
        # print("ID_DERNIER_TOUR DANS LA LISTE:",elms[2])
        '''IL FAUT SUPPRIMER LES N PREMIERS ELEMENTS DE LA LISTE'''
        print("LISTE DE TRAVAIL:", elms)
        for i in range(1, elms[0] + 1):
            """ajout des matches manquants"""
            # print(elms[3][0][trouver+i-1])
            print(elms[3][0])
            Controlertournoi.saisir_match(elms[3][0], elms[2], elms[1], boucle=nbrmanquant, mode='i')

    @staticmethod
    def compt_tour(ID_TOURNOI_COURS):
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        # element = Query()
        # nresult = []
        nresult = list(map(lambda x: x["id tournois"], tour_table.all()))
        # print(nresult)
        tour = nresult.count(ID_TOURNOI_COURS)
        # print(tour)
        if tour == 0:
            tour += 1
        elif tour == 1:
            tour += 1
        elif tour == 2:
            tour += 1
        elif tour == 3:
            tour += 1
        elif tour >= 4:
            print("On a déjà", tour, "tours")
            sys.exit()
        else:
            print("non valide")
            print(nresult)
            sys.exit()
        return tour

    @staticmethod
    def saisir_match(t1, tr_id, IDTOURNOISENCOURS, boucle=4, mode=None):
        """Saisi du résultat."""
        # Créer le Match avant le remplissage.
        print("====>Les ID DES JOUEURS SONT<====:", t1)
        tr_id = Controlertournoi.id_tour(IDTOURNOISENCOURS)
        print("saisir:\n (G): pour Gagner\n (N): pour Nul\n (P): pour Perdu")
        for i in range(0, boucle):
            globals()['resultat%s' % i] = input(f"saisir le résultat du match{i + 1} pour le joueur N°1").lower()
            if globals()['resultat%s' % i] == "g":
                print(['resultat%s' % i])
                print(t1[i][0], ": +1")
                global id_j1
                id_j1 = t1[i][0]
                print(t1[i][1], ": +1")
                global id_j2
                id_j2 = t1[i][1]
                resultat = joueurs_table.search(where('Identifiant du joueur') == t1[i][0])
                resultat = str(resultat)
                print('==> Le RESULTAT VAUT FCT SAISIR MATCH:', resultat, '<==')
                bddscore = int(resultat[len(str(resultat)) - 3:len(str(resultat)) - 2])
                print('==> Le BDDSCORE VAUT FCT SAISIR MATCH:', bddscore, '<==')
                joueurs_table.update({'Score du joueur': bddscore + 1}, where('Identifiant du joueur') == t1[i][0])
                # print("======>ID JOUEUR1  FCT SAISIR MATCH<=====:",t1[i][0])
                # print("======>ID JOUEUR2 :<=====", t1[i][1])
                # print("======>N° TOUR :<=====", tr_id[-1])
                print("======>N° TOURNOIS :<=====", IDTOURNOISENCOURS)
                # db.insert(Document({'name': 'John', 'age': 22}, doc_id=12))
                # match_table.insert("G", "P",t1[i][0], t1[i][1],id_tour,IDTOURNOISENCOURS,['id du match']=tr_id)
                if mode == 'i':
                    match_table.insert({'id du match': str(uuid.uuid1()), 'resultat du match Joueur 1': "G",
                                        'resultat du match Joueur 2': "P",
                                        'id du joueur1': t1[i][0], 'id du joueur2': t1[i][1],
                                        'id tour': id_Tour_transmettre,
                                        'id tournois': IDTOURNOISENCOURS})
                else:
                    Tournoi.creermatch("G", "P", t1[i][0], t1[i][1], tr_id[-1], IDTOURNOISENCOURS)
                print('====================================ICI=====================================')
                print(f"ajouter+1 au joueur1 dans la bdd pour le matcht N°{i + 1}")
            elif globals()['resultat%s' % i] == "p":
                print(['resultat%s' % i])
                print(t1)
                print(t1[i][0], ": =0")
                # global id_j1
                id_j1 = t1[i][0]
                print(t1[i][1], ": =1")
                # global id_j2
                id_j2 = t1[i][1]
                resultatp = joueurs_table.search(where('Identifiant du joueur') == t1[i][0])
                resultatp = str(resultatp)
                print('==> Le RESULTAT VAUT FCT SAISIR MATCH:', resultatp, '<==')
                bddscorep = int(resultatp[len(str(resultatp)) - 3:len(str(resultatp)) - 2])
                print('==> Le BDDSCORE VAUT FCT SAISIR MATCH:', bddscorep, '<==')
                joueurs_table.update({'Score du joueur': bddscorep + 1}, where('Identifiant du joueur') == t1[i][0])
                # print("======>ID JOUEUR1  FCT SAISIR MATCH<=====:",t1[i][0])
                # print("======>ID JOUEUR2 :<=====", t1[i][1])
                # print("======>N° TOUR :<=====", tr_id[-1])
                # print("======>N° TOURNOIS :<=====", IDTOURNOISENCOURS)
                if mode == 'i':
                    match_table.insert({'id du match': str(uuid.uuid1()), 'resultat du match Joueur 1': "P",
                                        'resultat du match Joueur 2': "G",
                                        'id du joueur1': t1[i][0], 'id du joueur2': t1[i][1],
                                        'id tour': id_Tour_transmettre,
                                        'id tournois': IDTOURNOISENCOURS})
                else:
                    Tournoi.creermatch("P", "G", t1[i][0], t1[i][1], tr_id[-1], IDTOURNOISENCOURS)
                    # Tournoi.creermatch("G", "P", t1[i][0], t1[i][1], tr_id[-1], IDTOURNOISENCOURS)
                print(f"ajouter+1 au joueur2 dans la bdd pour le matcht N°{i + 1}")
            elif globals()['resultat%s' % i] == "n":
                print(['resultat%s' % i])
                print(t1[i][0], ": =+0.5")
                # global id_j1
                id_j1 = t1[i][0]
                print(t1[i][1], ": =+0.5")
                # global id_j2
                id_j2 = t1[i][1]
                resultatn = joueurs_table.search(where('Identifiant du joueur') == t1[i][0])
                resultatn = str(resultatn)
                print('==> Le RESULTAT VAUT FCT SAISIR MATCH:', resultatn, '<==')
                bddscoren = int(resultatn[len(str(resultatn)) - 3:len(str(resultatn)) - 2])
                print('==> Le BDDSCORE VAUT FCT SAISIR MATCH:', bddscoren, '<==')
                joueurs_table.update({'Score du joueur': bddscoren + 0.5}, where('Identifiant du joueur') == t1[i][0])
                resultatnn = joueurs_table.search(where('Identifiant du joueur') == t1[i][1])
                resultatnn = str(resultatnn)
                bddscorenn = int(resultatnn[len(str(resultatnn)) - 3:len(str(resultatnn)) - 2])
                joueurs_table.update({'Score du joueur': bddscorenn + 0.5}, where('Identifiant du joueur') == t1[i][1])
                print(f"ajouter+1/2 au joueur2 dans la bdd pour le matcht N°{i + 1}")
                print(f"ajouter+1/2 au joueur1 dans la bdd pour le matcht N°{i + 1}")
                # print("======>ID JOUEUR1  FCT SAISIR MATCH<=====:",t1[i][0])
                # print("======>ID JOUEUR2 :<=====", t1[i][1])
                # print("======>N° TOUR :<=====", tr_id[-1])
                # print("======>N° TOURNOIS :<=====", IDTOURNOISENCOURS)
                if mode == 'i':
                    match_table.insert({'id du match': str(uuid.uuid1()), 'resultat du match Joueur 1': "N",
                                        'resultat du match Joueur 2': "N",
                                        'id du joueur1': t1[i][0], 'id du joueur2': t1[i][1],
                                        'id tour': id_Tour_transmettre,
                                        'id tournois': IDTOURNOISENCOURS})
                else:
                    Tournoi.creermatch("N", "N", t1[i][0], t1[i][1], tr_id[-1], IDTOURNOISENCOURS)
                    # Tournoi.creermatch("P", "G", t1[i][0], t1[i][1], tr_id[-1], IDTOURNOISENCOURS)
            else:
                print(['resultat%s' % i])
                print("saisie non comprise")

    @staticmethod
    def genererpairejoueur():
        """Générer des paires de joueurs."""
        lstmatches = Tournoi.aparaige(ID_TOURNOI_ENCOURS)
        print(lstmatches)

    @staticmethod
    def lancertournoi():
        """Amorçage du tournois."""
        lstIdToutnois = Controlertournoi.lstidtournois(tournois_table)
        global lstIdParticipant
        lstIdParticipant = Controlertournoi.selectionparticipant(8)

        if not lstIdToutnois:
            Joueur.message("Vous devez créer au moins un tournois")
            sys.exit()
        else:
            print(lstIdToutnois[0])
            print(lstIdParticipant)
            global ID_TOURNOI_ENCOURS
            ID_TOURNOI_ENCOURS = lstIdToutnois[0]
            Tournoi.inscriptionparticipants(lstIdParticipant, lstIdToutnois[0])
            Joueur.message("Lancement du tournois ok")

    @staticmethod
    def premiertour():
        """Lancer le premierTour."""
        print("TOURNOI En COURS", ID_TOURNOI_ENCOURS)
        print("PARTICIPANT", lstIdParticipant)
        lstmatches = Tournoi.aparaige(ID_TOURNOI_ENCOURS)
        tr_id = Controlertournoi.id_tour(ID_TOURNOI_ENCOURS)
        nbrtr = Controlertournoi.compt_tour(ID_TOURNOI_ENCOURS)
        Tournoi.creertour(nbrtr, ID_TOURNOI_ENCOURS, lstmatches)
        print(tr_id)
        Controlertournoi.saisir_match(lstmatches, tr_id, ID_TOURNOI_ENCOURS)

    @staticmethod
    def debuter():
        """Amrocage."""
        Controlertournoi.premiertour()
        # print("terminer", ID_TOURNOI_ENCOURS)

    @staticmethod
    def fermer():
        """Fermeture."""
        afaire = Ihm.loadertournois()
        if afaire == "o":
            afermer = input("RENSEIGNER L'ID TOUR:")
            print(afermer)
            Controlertournoi.maj(afermer)
        elif afaire == "n":
            print("Au revoir")


class Controleurmenu:
    """Initialisation du controleur du menu général."""

    def __init__(self, nom):
        """Constructeur."""
        self.nom = nom

    def gestionchoix(self):
        """Exécution des méthodes en fonction du choix du menu."""
        validationchoix = Ihm.saisie_user()  # views.View.saisie_user()
        global selctionmem
        selctionmem = validationchoix

        if validationchoix == 1:
            print()
            print('========vous avez choisi le tournois========\n')
            t = Ihm.creat_tournoi()
            trns.creation_tournoi(t)
            trns.inserer_bdd('tournois')
            self.gestionchoix()

        elif validationchoix == 2:
            print()
            print('\n========vous avez choisi ajouter joueur( s )========\n')

            Controleurjoueurs.creation_joueurs()
            self.gestionchoix()
        elif validationchoix == 3:
            print()
            print('========vous avez choisi de lancer un tournois========\n')
            Controlertournoi.lancertournoi()
            self.gestionchoix()

        elif validationchoix == 4:
            print()
            print('========vous avez choisi lancer les matchs========\n')
            Controlertournoi.debuter()
            self.gestionchoix()

        elif validationchoix == 5:
            print()
            print('========vous avez choisi le Rapport des joueurs========\n')
            Ihm.rapportjoueurs()
            self.gestionchoix()

        elif validationchoix == 6:
            print()
            print('========vous avez choisi le rapport des joueurs par score========\n')
            print(Ihm.triejoueur2('s'))
            self.gestionchoix()

        elif validationchoix == 7:
            print("\n========vous avez choisi Rapport des tournois========\n")
            Ihm.rapporttournois()
            self.gestionchoix()

        elif validationchoix == 8:
            print()
            print("========vous avez choisi Rapport des matchs d'un tournois========\n")
            Ihm.rapportmatchs()
            self.gestionchoix()

        elif validationchoix == 9:
            print()
            print("Vous avez choisi le Rapport des tours d'un tournois")
            Ihm.rapporttours()
            self.gestionchoix()

        elif validationchoix == 10:
            print()
            print('Vous avez choisi de Reprendre un match')
            # Controlertournoi.fermer()
            Controlertournoi.acompleter()
            self.gestionchoix()

        elif validationchoix == 11:
            print()
            print('Vous avez choisi de Quitter le programme')
            ctrlg = Controlermenugestion()
            ctrlg.sortir()
            '''
        elif validationchoix == 12:
            print()
            print('Vous avez choisi de Reprendre le programme')
            # ctrlg = Controlermenugestion()
            # ctrlg.sortir()
            Maincontroller.reprise()
            '''
        else:
            print('choix invalides')


atexit.register(Maincontroller.handler)

if __name__ == "__main__":
    # pass
    # menu = Maincontroller()
    # menu.demarrer()
    # Controlertournoi.lancertournoi()
    # signal.signal(signal.SIGHUP, Maincontroller.handler)
    # signal.signal(signal.SIGINT, Maincontroller.handler)
    # signal.signal(signal.SIGTERM, Maincontroller.handler())
    # atexit.register(Maincontroller.handler)
    # Controlertournoi.debuter()
    # print("id en cours: ", ID_TOURNOI_ENCOURS)
    # print(Controlertournoi.id_tour("45c0626e-2ce0-11ed-bd8e-3af9d3a77849"))
    # print(Controlertournoi.genererpairejoueur())
    # Controlertournoi.premiertour()
    # print(Controlertournoi.compt_tour("e212e336-276c-11ed-8c32-acde48001122"))
    # print("liste des idJoueurs: ", Controlertournoi.selectionparticipant(8))
    # print("liste des tournois: ", Controlertournoi.lstidtournois(tournois_table))
    # Maincontroller.idtournoiencours()
    # print('Nombre de tour égal:',Controlertournoi.compt_tour("f4540b56-56e2-11ed-8d4c-acde48001122"))
    # print('nombre de tour egale:',Controlertournoi.id_tour("f4540b56-56e2-11ed-8d4c-acde48001122"))
    # print('Liste des Matchs:',Controlertournoi.donnerLstMatchs())
    # print('Les Matchs manquants:',Controlertournoi.matchmanquant())
    Controlertournoi.acompleter()
    # Maincontroller.selectionJoueurs()
    # print(tournois_table.all())
