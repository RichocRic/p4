"""Models."""
import itertools
import os
import random
import uuid
from datetime import date, datetime
from tinydb import TinyDB, where, Query

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

jdb = TinyDB('../joueurs.json')
db = TinyDB('../database.json')
sdb = TinyDB('../savedb.json')

# jdb = TinyDB('../bdd/joueurs.json')
# db = TinyDB('../bdd/database.json')
# sdb = TinyDB('../bdd/savedb.json')
joueurs_table = jdb.table('joueurs')
tournois_table = db.table('tournois')
match_table = db.table('match')
tour_table = db.table('tour')

sdbjoueurs_table = sdb.table('sdbjoueurs')
sdbtournois_table = sdb.table('sdbtournois')
sdbmatch_table = sdb.table('sdbmatch')
sdbtour_table = sdb.table('sdbtour')
today = date.today()
confirm_msg = ['INSERTION TERMINEE', 'CREATION TERMINEE']
IDTOURNOISENCOURS = " "
IDJOUEURSSELECT = " "

"""chaque joueur devrait contenir au moins les données suivantes :
Nom de famille
Prénom
Date de naissance
Sexe
Classement
Il s'agit d'un chiffre positif.
"""


class Joueur:
    """Classe Joueur."""

    def __init__(self, name=None,
                 lastname=None,
                 birthday=None,
                 genre=None,
                 rang=None,
                 score=0):
        """Constructeur."""
        self.joueur_id = str(uuid.uuid1())
        self.nom = name
        self.prenom = lastname
        self.date_naissance = birthday
        self.sexe = genre
        self.classement = rang
        self.score = score

    def creation_joueur(self, j):
        """Création du joueur."""
        self.nom = j[0]
        self.prenom = j[1]
        self.date_naissance = j[2]
        self.sexe = j[3]
        self.classement = j[4]

    def serialiser(self):
        """Json2 variable."""
        info_joueur = {"Identifiant du joueur": self.joueur_id, "Nom du joueur": self.nom,
                       "Prénom du joueur": self.prenom, "Âge du joueur": self.date_naissance,
                       "Sexe du joueur": self.sexe, "Classement du joueur": self.classement, "Score du joueur": 0}
        return info_joueur

    @staticmethod
    def message(msg):
        """Custo MSG."""
        print('=========================' + msg + '=========================')

    def inserer_bdd(self, nomtable):
        """Insert into DB."""
        jdb.table(nomtable).insert(self.serialiser())
        Joueur.message(confirm_msg[0])

    @staticmethod
    def deserialiser(joueur_serialiser):
        """De Json vers variabl."""
        joueur_id = joueur_serialiser["Identifiant du joueur"]
        nom = joueur_serialiser["Nom du joueur"]
        prenom = joueur_serialiser["Prénom du joueur"]
        date_naissance = joueur_serialiser["Âge du joueur"]
        sexe = joueur_serialiser["Sexe du joueur"]
        classement = joueur_serialiser["Classement du joueur"]
        return Joueur(joueur_id, nom, prenom, date_naissance, sexe, classement)


class Tournoi:
    """Creation tournois."""

    def __init__(self, participants=None,
                 nom_tournois=None,
                 lieu_tournois=None,
                 date_tournois=None,
                 nbr_tour=4,
                 joueur_id=None,
                 ctrl_temps=None,
                 description_tournois=None):
        """Constructeur."""
        self.tournois_id = str(uuid.uuid1())
        self.nom = nom_tournois
        self.lieu = lieu_tournois
        self.date = date_tournois
        self.nbr_tour = nbr_tour
        self.ctrl_temps = ctrl_temps
        self.joueur_id = joueur_id
        self.participants = participants
        self.description = description_tournois
        # self.list2tour = []

    def creation_tournoi(self, t):
        """Summary_Création du tournois."""
        self.nom = t[0]
        self.lieu = t[1]
        self.date = t[2]
        self.nbr_tour = t[3]
        self.participants = t[4]
        self.ctrl_temps = t[5]
        self.description = t[6]

    def serialiser_tournoi(self):
        """Serialisation."""
        info_tournoi = {"id du tournois": self.tournois_id, "nom du tournois": self.nom, "lieu du tournois": self.lieu,
                        "date du tournois": self.date, "nombre de tour": self.nbr_tour,
                        "contrôle de temps": self.ctrl_temps, "id des joueurs": self.joueur_id,
                        "nombre de participants": self.participants, "la description du tournois": self.description}
        return info_tournoi

    def inserer_bdd(self, nomtable):
        """Insert into DB."""
        db.table(nomtable).insert(self.serialiser_tournoi())
        Joueur.message(confirm_msg[0])

    @staticmethod
    def participantss(nbr_joueurs):
        """Récupération des id joueurs dans la table joueur."""
        doc_ids = []
        id_joueurs = []
        for entry in joueurs_table.all():
            doc_ids.append([entry['Identifiant du joueur'],
                            entry['Nom du joueur'],
                            entry['Classement du joueur'],
                            entry['Score du joueur']])
        print(len(doc_ids))
        print("filtre des joueurs: ", doc_ids)
        print()
        listparticipant = random.sample(doc_ids, int(nbr_joueurs))
        print("LE TYPE EST: ", type(listparticipant))
        print("liste des participants: ", listparticipant)
        for j in listparticipant:
            id_joueurs.append(j[0])
        print()
        print("id des joueurs: ", id_joueurs)
        global IDJOUEURSSELECT
        IDJOUEURSSELECT = id_joueurs
        tournois_table.update({'id des joueurs': id_joueurs}, where('id du tournois') == IDTOURNOISENCOURS)
        return listparticipant

    @staticmethod
    def inscriptionparticipants(joueursid, tournoisid):
        """Inscription des joueurs dans tournois."""
        tournois_table.update({'id des joueurs': joueursid}, where('id du tournois') == tournoisid)

    @staticmethod
    def recupidjoueurs():
        """RECUPERER LES ID JOUEURS DEPUIS LA TABLE TOURNOIS EN COURS."""
        Tournoi.participantss(8)
        element = Query()
        nresult = []
        result = tournois_table.search(element['id du tournois'] == IDTOURNOISENCOURS)
        for entry in result:
            nresult.append(entry['id des joueurs'])
        print()
        print("LES ID DES JOUEURS POUR CE TOURNOIS DEPUIS LA TABLE SONT: ==>", nresult)
        return nresult

    @staticmethod
    def razscore():
        """Supprimer les scores à la fin du tournois."""
        doc_ids = []
        for entry in joueurs_table.all():
            doc_ids.append(entry['Identifiant du joueur'])
        print(len(doc_ids))
        print(doc_ids)
        for count, i in enumerate(doc_ids):
            print(doc_ids[count])
            joueurs_table.update({'Score du joueur': 0}, where('Identifiant du joueur') == doc_ids[count])

    def recupclassement(self, valeur):
        """Trier par classement, score, ou bien par nom."""
        lstparticipantss = self.participantss(8)
        # clssmnt = []
        str(valeur)
        if valeur is str("c"):
            clssmnt = sorted(lstparticipantss, key=lambda x: x[2], reverse=True)
        elif valeur is str("s"):
            # clssmnt = sorted(lstparticipantss, key=lambda x: x[3], reverse=True)
            clssmnt = sorted(lstparticipantss, key=lambda x: x[2], reverse=True)
        else:
            print('demande non comprise')
            clssmnt = sorted(lstparticipantss, key=lambda x: x[1], reverse=True)
        return clssmnt

    @staticmethod
    def donner_temps(valeur):
        """Date ou Heure."""
        temps = str(datetime.now())
        if valeur == 'j':
            moment = temps[:11]
        elif valeur == 'h':
            moment = temps[11:]
        else:
            print('saisie non comprise')
        return moment

    @staticmethod
    def recupinfotournois():
        """Récupérer les informationstournois pour la création des tours et matchs."""
        global nbrtour, id_tournois, nbr_participants
        resultat = tournois_table.search(where('id du tournois') == IDTOURNOISENCOURS)
        information_tournois = []
        if not resultat:
            Joueur.message("Aucun tournois de ce nom")
        else:
            for entry in resultat:
                nbrtour = int(entry["nombre de tour"])
                id_tournois = entry["id du tournois"]
                nbr_participants = int(entry["nombre de participants"])
        information_tournois.append(nbrtour)
        information_tournois.append(id_tournois)
        information_tournois.append(nbr_participants)
        return information_tournois

    @staticmethod
    def creertour(nbrtoure, lstmatch, IDTOURNOISENCOURS):
        """Creation tour."""
        tour = Tour("Round" + str(nbrtoure), "", "", lstmatch, IDTOURNOISENCOURS)
        tour.inserer_bdd('tour')

    @staticmethod
    def creermatch(resultattwo, resultatone, joueurone, joueurtwo, id_trs, IDTOURNOISENCOURS):
        """Creation du match."""
        m1 = Match(resultattwo, resultatone, joueurone, joueurtwo, id_trs, IDTOURNOISENCOURS)
        m1.inserer_bdd('match')

    @staticmethod
    def lstidtournois(table):
        """Retourne la liste des id Tournois."""
        doc_ids = []
        for entry in table.all():
            if table == tournois_table:

                doc_ids.append(entry['id du tournois'])
            elif table == tour_table:
                doc_ids.append(entry['id tournois'])
        return doc_ids

    @staticmethod
    def combiendetour():
        """Donne le nombre de tour pour un tournois entre 0 et 4."""
        element = Query()
        nresult = []
        result = tour_table.search(element['id tournois'] == IDTOURNOISENCOURS)
        for entry in result:
            nresult.append(entry['nom du tour'])
        print("LE NOMBRE DE TOUR POUR CE TOURNOIS EST: ", len(nresult))
        print(nresult)
        if len(nresult) == 0:
            max_value = 0
            print(max_value)
        elif len(nresult) > 1 & len(nresult) == 3:
            res = [elem.replace('Tour', '') for elem in nresult]
            res = [int(x) for x in res]
            print(res)
            max_value = max(res)
            print("LE MAXIMUM EST: ", max_value)
        elif len(nresult) > 4 | len(nresult) == 4:
            # cloturer le tournois
            res = [elem.replace('Tour', '') for elem in nresult]
            res = [int(x) for x in res]
            print(res)
            max_value = max(res)
            print("TOURNOIS A CLOTURER")
        else:
            res = [elem.replace('Tour', '') for elem in nresult]
            res = [int(x) for x in res]
            print(res)
            max_value = max(res)
            print("LE MAXIMUM EST: ", max_value)
        return max_value

    @staticmethod
    def listidtourcourant():
        """Récupération du tour courant."""
        tour_ids = []
        for entry in tour_table.all():
            tour_ids.append(entry['id du tour'])
        print("TOURS_EN COURS", tour_ids)
        if int(len(tour_ids)) == 0:
            print('c vide')
        elif int(len(tour_ids)) == 1:
            tour_ids = tour_ids
            print("TOURS_EN COURS", tour_ids)
        elif int(len(tour_ids)) > 1:
            tour_ids = tour_ids[-1]
            print("TOURS_EN COURS: ==>", tour_ids)
        return tour_ids

    def recuplstmatch(self):
        """Recupération des listes matches."""
        trs_encours = self.listidtourcourant()
        print("RECUPERATION DE L'ID TOUR:==>", trs_encours)
        nresult = []
        element = Query()
        resultatlst = tour_table.search(element['id du tour'] == trs_encours)
        for entry in resultatlst:
            nresult.append(entry['liste des matches'])
        # print(tour_table.search(element['date de fin'] == trs_encours))
        print("RECUPERATION DE LA LISTE DES MATCHES:==>", nresult)
        return nresult

    def termine(self, lstrescue):
        """Faire un horodatage si la reponse est oui."""
        trs_encours = self.listidtourcourant()
        response = input("TERMINEE ? (O/N) ").lower()
        if response == "o":
            ddfin = str(Tournoi.donner_temps('j'))
            tour_table.update({'date de fin': ddfin}, where('id du tour') == trs_encours)
            print("DFIN: ", ddfin)
            hdfin = str(Tournoi.donner_temps('h'))
            tour_table.update({'heure de fin': hdfin}, where('id du tour') == trs_encours)
            print("HFIN: ", hdfin)
            lstm = self.recuplstmatch()
            if not lstm:
                lstm = list(lstrescue)
                print("LISTE RESCUE BRUTE: ", lstm)
                res = list(map(list, lstm))
                print("LISTE  RESCUE CONVERTI en LST DE LISTE: ", res)
            else:
                res = itertools.chain(*lstm)
                res = list(res)
                print("CONVERSION EN LISTE TUPLE 2 :", res)
            self.saisir_match(res, trs_encours)

    def saisir_match(self, t1, tr_id):
        """Saisi du résultat."""
        # Créer le Match avant le remplissage.
        print("saisir:\n (G): pour Gagner\n (N): pour Nul\n (P): pour Perdu")
        for i in range(0, 4):
            globals()['resultat%s' % i] = input(f"saisir le résultat du match{i + 1} pour le joueur N°1").lower()
            if globals()['resultat%s' % i] == "g":
                print(['resultat%s' % i])
                print(t1[i][0], ": +1")
                print(t1[i][1], ": +1")
                resultat = joueurs_table.search(where('Identifiant du joueur') == t1[i][0])
                resultat = str(resultat)
                bddscore = int(resultat[len(str(resultat)) - 3:len(str(resultat)) - 2])
                joueurs_table.update({'Score du joueur': bddscore + 1}, where('Identifiant du joueur') == t1[i][0])
                self.creermatch("G", "P", t1[i][0], t1[i][1], tr_id)
                print(f"ajouter+1 au joueur1 dans la bdd pour le matcht N°{i + 1}")
            elif globals()['resultat%s' % i] == "p":
                print(['resultat%s' % i])
                print(t1[i][0], ": =0")
                print(t1[i][1], ": =1")
                resultatp = joueurs_table.search(where('Identifiant du joueur') == t1[i][0])
                resultatp = str(resultatp)
                bddscorep = int(resultatp[len(str(resultatp)) - 3:len(str(resultatp)) - 2])
                joueurs_table.update({'Score du joueur': bddscorep + 1}, where('Identifiant du joueur') == t1[i][0])
                self.creermatch("P", "G", t1[i][0], t1[i][1], tr_id)
                print(f"ajouter+1 au joueur2 dans la bdd pour le matcht N°{i + 1}")
            elif globals()['resultat%s' % i] == "n":
                print(['resultat%s' % i])
                print(t1[i][0], ": =+0.5")
                print(t1[i][1], ": =+0.5")
                resultatn = joueurs_table.search(where('Identifiant du joueur') == t1[i][0])
                resultatn = str(resultatn)
                bddscoren = int(resultatn[len(str(resultatn)) - 3:len(str(resultatn)) - 2])
                joueurs_table.update({'Score du joueur': bddscoren + 0.5}, where('Identifiant du joueur') == t1[i][0])
                resultatnn = joueurs_table.search(where('Identifiant du joueur') == t1[i][1])
                resultatnn = str(resultatnn)
                bddscorenn = int(resultatnn[len(str(resultatnn)) - 3:len(str(resultatnn)) - 2])
                joueurs_table.update({'Score du joueur': bddscorenn + 0.5}, where('Identifiant du joueur') == t1[i][1])
                print(f"ajouter+1/2 au joueur2 dans la bdd pour le matcht N°{i + 1}")
                print(f"ajouter+1/2 au joueur1 dans la bdd pour le matcht N°{i + 1}")
                self.creermatch("N", "N", t1[i][0], t1[i][1], tr_id)
            else:
                print(['resultat%s' % i])
                print("saisie non comprise")

    @staticmethod
    def diviser(lst):
        """Couper en 2."""
        grp_one = lst[len(lst) // 2:]
        grp_two = lst[:len(lst) // 2]
        return grp_two, grp_one

    def generermatch(self, lst1, lst2):
        """Création des Matches."""
        list_dematches = []
        dejajoue = []
        tour_actuel = self.lstidtournois(tour_table)
        tour_actuel = len(tour_actuel)
        print("le nombre de tour", tour_actuel)
        for rang in range(len(lst1)):
            match = lst1[rang], lst2[rang]
            list_dematches.append(match)
        print(f"LISTE DES MATCHES DU ROUND{tour_actuel + 1}: ", list_dematches)
        dejajoue.append(list_dematches)
        listdematches = self.aparaige(IDTOURNOISENCOURS)
        self.creertour(tour_actuel + 1, listdematches)
        self.termine(listdematches)

    def debuter(self):
        """Commencer le premier tour."""
        global IDTOURNOISENCOURS
        lstidtournois = self.lstidtournois(tournois_table)
        lstidtour = self.lstidtournois(tour_table)
        lstidtour.count(IDTOURNOISENCOURS)
        print("ID des tours", lstidtour)
        print(len(lstidtour))
        print("ID des tournois", lstidtournois)
        if len(lstidtournois) == 0:
            print('Vous devez créer au moins un tournois')
        else:
            nlstidtournois = []
            if lstidtour.count(IDTOURNOISENCOURS) == 0:
                IDTOURNOISENCOURS = random.choice(lstidtournois)
                print("choix du tournois: ", IDTOURNOISENCOURS)
            else:
                for x in lstidtour:
                    for y in lstidtournois:
                        if x == y:
                            lstidtournois = lstidtournois.remove(y)
                        else:
                            nlstidtournois.append(lstidtournois)
                print("NOUVELLE LISTE: ", nlstidtournois)
                IDTOURNOISENCOURS = random.choice(nlstidtournois)
                rendu = random.randint(0, len(IDTOURNOISENCOURS))
                IDTOURNOISENCOURS = IDTOURNOISENCOURS[rendu]
                print("ID: ", IDTOURNOISENCOURS)
        info = self.recupinfotournois()
        print(info)
        # lstparticpantstournois = self.participantss(info[2])
        print('nombre de participants selectionné: ', IDJOUEURSSELECT)
        # création des groupes
        id_joueurbdd = self.recupidjoueurs()
        id_joueurbdd = itertools.chain(*id_joueurbdd)
        id_joueurbdd = list(id_joueurbdd)
        print("ID JOUEUR DEPUIS TBL TOURNOIS", id_joueurbdd)
        tbl_one, tbl_two = self.diviser(id_joueurbdd)
        # tbl_one, tbl_two = self.diviser(IDJOUEURSSELECT)
        print("Tableau1: ", tbl_one)
        print("Tableau2: ", tbl_two)
        self.generermatch(tbl_one, tbl_two)

    @staticmethod
    def aparaige(idtournois):
        """Creation des paires."""
        element = Query()
        result = match_table.search(element['id tournois'] == idtournois)
        print("résultat Apairage: ", result)
        tour_en_cours = len(result) // 4 + 1
        liste_anciens_matchs = list(map(lambda x: [x['id du joueur1'], x['id du joueur2']], result))
        result = tournois_table.search(element['id du tournois'] == idtournois)
        print("résultat Apairage 2: ", result)
        liste_joueurs = result[0]['id des joueurs']
        liste_joueurs = list(
            map(lambda x: joueurs_table.search(element['Identifiant du joueur'] == x)[0], liste_joueurs))
        liste_joueurs.sort(key=lambda x: x["Classement du joueur"], reverse=True)
        liste_joueurs.sort(key=lambda x: x["Score du joueur"], reverse=True)
        liste_joueurs = list(map(lambda x: x["Identifiant du joueur"], liste_joueurs))
        # print(liste_joueurs)
        # liste_joueurs=["a","b","c","d","e","f","g","h"]
        d = liste_joueurs
        # liste_anciens_matchs=[["a","b"],["b","c"],["e","h"],["a","g"]]
        d1 = liste_anciens_matchs
        d2 = []
        for i in range(8):
            for j in range(i + 1, 8):
                if [d[i], d[j]] not in d1:
                    d2.append([d[i], d[j], i + j])
        d2.sort(key=lambda x: x[2], reverse=True)

        def check_player_exist(list_matchs, match):
            """Vérifie si deja ensemble."""
            for num in list_matchs:
                if match[0] == num[0] or match[0] == num[1] or match[1] == num[0] or match[1] == num[1]:
                    return False
            return True

        def add_elem(big_list, indexy, small_list):
            """Gestion des liste."""
            for jum in range(indexy + 1, len(big_list)):
                if len(small_list) > indexy:
                    small_list.pop()
                if check_player_exist(small_list, big_list[jum]):
                    small_list.append(big_list[jum])
                    if len(small_list) == 4:
                        return small_list
            return add_elem(big_list)

        def list_comb(list_combe):
            """Si 1-->2 ko alors 1-->3."""
            list2 = []
            for lim in range(len(list_combe)):
                if len(list2) > 0:
                    list2.pop()
                list2.append(list_combe[lim])
                for jim in range(lim + 1, len(list_combe)):
                    if len(list2) > 1:
                        list2.pop()
                    if check_player_exist(list2, list_combe[jim]):
                        list2.append(list_combe[jim])
                        for k in range(jim + 1, len(list_combe)):
                            if len(list2) > 2:
                                list2.pop()
                            if check_player_exist(list2, list_combe[k]):
                                list2.append(list_combe[k])
                                for lam in range(k + 1, len(list_combe)):
                                    if len(list2) > 3:
                                        list2.pop()
                                    if check_player_exist(list2, list_combe[lam]):
                                        list2.append(list_combe[lam])
                                        return list2
            return -1

        if tour_en_cours > 4:
            return -1
        if tour_en_cours > 1:
            lstcombi = list(map(lambda x: [x[0], x[1]], list_comb(d2)))
        else:
            lstcombi = list(map(lambda x: [liste_joueurs[x], liste_joueurs[x + 4]], range(4)))
        return lstcombi


"""
Chaque tour est une liste de matchs. Chaque match consiste en une paire de joueurs avec un champ de résultats
 pour chaque joueur.
Lorsqu'un tour est terminé, le gestionnaire du tournoi saisit les résultats de chaque match avant de générer
les paires suivantes.
Le gagnant reçoit 1 point, le perdant 0 point. Si un match se termine par un match nul, chaque joueur reçoit 1/2 point.
En plus de la liste des correspondances, chaque instance du tour doit contenir un champ de nom.
Actuellement, nous appelons nos tours "Round 1", "Round 2", etc.
Elle doit également contenir un champ Date et heure de début et un champ Date et heure de fin,
qui doivent tous deux être automatiquement remplis lorsque l'utilisateur crée un tour et le marque comme terminé.
Les instances de round doivent être stockées dans une liste sur l'instance de tournoi à laquelle elles appartiennent.
"""


class Match:
    """Class match."""

    def __init__(self, resultatjtwo=None,
                 resultatjone=None,
                 joueurone_id=None,
                 joueurtwo_id=None,
                 tour_id=None,
                 tournois_id=None):
        """Constructeur."""
        self.match_id = str(uuid.uuid1())
        self.resultatjtwo = resultatjtwo
        self.resultatjone = resultatjone
        self.joueurone_id = joueurone_id
        self.joueurtwo_id = joueurtwo_id
        self.tour_id = tour_id
        self.tournois_id = tournois_id

    def serialiser_match(self):
        """Serialiser le match."""
        info_match = {"id du match": self.match_id, "resultat du match Joueur 1": self.resultatjone,
                      "resultat du match Joueur 2": self.resultatjtwo, "id du joueur1": self.joueurone_id,
                      "id du joueur2": self.joueurtwo_id, "id tour": self.tour_id, "id tournois": self.tournois_id}
        return info_match

    @staticmethod
    def deserialiser_match(match_serialiser):
        """String match."""
        match_id = match_serialiser["id du match"]
        joueurone_id = match_serialiser["id du joueur1"]
        resultatjone = match_serialiser["resultat du match du joueur 1"]
        joueurtwo_id = match_serialiser["id du joueur2"]
        resultatjtwo = match_serialiser["resultat du match du joueur 2"]
        id_tour = match_serialiser["id du tour"]
        # tournois_id = match_serialiser["id du tournois"]
        return Match(match_id, joueurone_id, resultatjone, joueurtwo_id, resultatjtwo, id_tour)

    def inserer_bdd(self, nomtable):
        """Insert into DB."""
        db.table(nomtable).insert(self.serialiser_match())
        Joueur.message(confirm_msg[0])


class Tour:
    """Creation de la class tour."""

    def __init__(self, nom=None, date_fin=None, heure_fin=None, id_tournoiss=None, lstmatchs=None):
        """Constructeur."""
        self.tour_id = str(uuid.uuid1())
        self.round = nom
        self.d_debut = str(Tournoi.donner_temps('j'))
        self.h_debut = str(Tournoi.donner_temps('h'))
        self.d_fin = date_fin
        self.h_fin = heure_fin
        self.id_tournois = id_tournoiss
        self.lstmatchs = lstmatchs

    def serialiser_tour(self):
        """Serialiser le tour."""
        info_tour = {"id du tour": self.tour_id, "nom du tour": self.round, "date de début": self.d_debut,
                     "heure de début": self.h_debut, "date de fin": self.d_fin, "heure de fin": self.h_fin,
                     "id tournois": self.id_tournois, "liste des matches": self.lstmatchs}
        return info_tour

    def inserer_bdd(self, nomtable):
        """Insert into DB."""
        db.table(nomtable).insert(self.serialiser_tour())
        Joueur.message(confirm_msg[0])

    @staticmethod
    def deserialiser_tour(tour_serialiser):
        """Deserialiser."""
        tour_id = tour_serialiser["id du match"]
        dfin = tour_serialiser["id du joueur1"]
        ddebut = tour_serialiser["resultat du match du joueur 1"]
        hdebut = tour_serialiser["id du joueur2"]
        hfin = tour_serialiser["resultat du match du joueur 2"]
        # nom_tour = tour_serialiser["id du tour"]
        # id_tournoiss = tour_serialiser["id du tournois"]
        # lstmatchs = tour_serialiser["liste des matches"]
        return Tour(tour_id, ddebut, hdebut, dfin, hfin)

    @staticmethod
    def get_ids_joueurs():
        """Récupération des id joueurs dans la table joueur."""
        doc_ids = []
        for entry in joueurs_table.all():
            doc_ids.append(entry['Identifiant du joueur'])
        print(len(doc_ids))
        listparticipant = random.sample(doc_ids, 8)
        print("=" * 15)
        print("liste des participants=:", listparticipant)
        print("=" * 15)
        db.table('tournois').update({'participants du tournois': listparticipant}, doc_ids=[1])
        return doc_ids


if __name__ == "__main__":
    """t1 = Tour(Nom='touré1', Date_debut='12/11/2022', heure_debut='11:29', Date_fin='12/12/2022',
    heure_fin='19:29', id_tournois=1) print(t1.get_ids_joueurs()) t1.maj() j1 = Joueur("Narb","yomé",56,"F",45,
    0) #j1.rapportjoueurs() j1.rapportDunJoueur() """
    trns = Tournoi(participants="jean, michel", nom_tournois="Bordeau", lieu_tournois="Bordeau",
                   date_tournois="20/12/2024", nbr_tour=4, joueur_id="45,57", ctrl_temps="bullet",
                   description_tournois="On s")
    # trns.creerApairage("toto")#ok
    # trns= Tournoi()#ok
    # trns.creation_tournoi()#ok
    # trns.inserer_bdd('tournois')#ok
    # trns.clssmntScore()#ok
    # trns.triclssmnt()#ok
    # trns.creerApairage(0)
    # trns.participantss(8)#ok
    # trns.recupclassement("c")#ok
    # trns.creerApairage(0)#ok
    # trns.combienDetour()#ok
    trns.debuter()
    # trns.loaderTournois()#ok trns.razScore() print(trns.lstidtournois(tour_table)) trns.search()#ok
    # trns.recupIdJoueurs('05460aa6-020e-11ed-a3b3-acde48001122') trns.rapportTournois() print(
    # trns.recupInfoTournois()) tournois_table = db.table('tournois') t1 = Tour("tour1","","",
    # "05460aa6-020e-11ed-a3b3-acde48001122") t1.inserer_bdd('tour') m1 = Match("P","G",
    # "98c6cf4a-01aa-11ed-b118-acde48001122","c130e286-01aa-11ed-b118-acde48001122",
    # "941d472c-05e6-11ed-a7ce-acde48001122","05460aa6-020e-11ed-a3b3-acde48001122") m1.inserer_bdd('match')
