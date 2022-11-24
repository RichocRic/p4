"""Ihm du programme d'échecs."""
import sys
from tinydb import TinyDB, where, Query

sys.path.append("/Users/hhmbp/Documents/OC/P4/p4C/models")
sys.path.append("/Users/hhmbp/Documents/OC/P4/p4C/controlers")
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

db = TinyDB('../database.json')
jdb = TinyDB('../joueurs.json')

# jdb = TinyDB('../bdd/joueurs.json')
# db = TinyDB('../bdd/database.json')
# sdb = TinyDB('../bdd/savedb.json')
# joueurs_table = db.table('joueurs')
joueurs_table = jdb.table('joueurs')
tournois_table = db.table('tournois')
match_table = db.table('match')
tour_table = db.table('tour')


class Ihm:
    """Creation de la class view."""

    ljouee = []
    ltourn = []
    lstmenu = ["1.)  Créer un nouveau tournoi.\n",
               "2.)  Ajouter un/plusieurs joueurs.\n",
               "3.)  Lancer le tournois.\n",
               "4.)  Lancer les matchs.\n",
               "5.)  Rapport des joueurs (par ordre alphabétique).\n",
               "6.)  Rapport des joueurs (par classement).\n",
               "7.)  Rapport des tournois.\n",
               "8.)  Rapport des matchs d'un tournois.\n",
               "9.)  Rapport des tours d'un tournois.\n",
               "10.) Reprendre un match.\n",
               "11.) Sortir du programme\n\n"]

    # "12.) Reprise\n"

    # =========================                     =========================
    # ========================= JOUEURS AFFICHAGE  =========================
    # =========================                     =========================

    @staticmethod
    def mess(msg):
        """Custo MSG."""
        print('=========================' + msg + '=========================')

    @staticmethod
    def rapportjoueurs():
        """Rapport Global."""
        Ihm.mess("==================================RAPPORT JOUEURS==================================")
        if not match_table.all():
            print('Pas de rapport ')
        else:
            print()
            print("Nom du joueur: ".ljust(10), "Prénom du joueur: ".ljust(10), "Âge du joueur: ".ljust(10),
                  "Sexe du joueur: ".ljust(10), "Classement du joueur: ".ljust(10),
                  "Score du joueur: ", )
            print()
            for entry in joueurs_table.all():
                # "Identifiant du joueur: ", entry["Identifiant du joueur"]+"| |"
                print(
                    entry["Nom du joueur"].ljust(17),
                    entry["Prénom du joueur"].ljust(17),
                    str(entry["Âge du joueur"]).ljust(17),
                    entry["Sexe du joueur"].ljust(17),
                    str(entry["Classement du joueur"]).ljust(20),
                    str(entry["Score du joueur"]).ljust(25)
                )

    @staticmethod
    def triejoueur2(valeur):
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
            print('Nom du joueur | |', 'Prénom du joueur | |', 'Âge du joueur | |', 'Sexe du joueur | |', 'Classement '
                                                                                                          'du joueur '
                                                                                                          '| |',
                  'Score du joueur | |')
            for entry in clssmnt:
                print(
                    entry["Nom du joueur"].ljust(17),
                    entry["Prénom du joueur"].ljust(20),
                    str(entry["Âge du joueur"]).ljust(20),
                    entry["Sexe du joueur"].ljust(20),
                    str(entry["Classement du joueur"]).ljust(20),
                    str(entry["Score du joueur"]).ljust(20),
                )
        else:
            print('demande non comprise')
            clssmnt = sorted(joueurs_table.all(), key=lambda x: x['Identifiant du joueur'], reverse=True)
        return

    @staticmethod
    def rapportdunjoueur():
        """Rapport joueur."""
        Ihm.mess("RAPPORT PAR JOUEUR")
        print()
        recherchenom = input("saisir le nom du joueur recherché: ").lower()
        resultat = joueurs_table.search(where('Nom du joueur') == recherchenom)
        if not resultat:
            Ihm.mess("Aucun joueur de ce nom")
        else:
            for entry in resultat:
                print(
                    "Nom du joueur: ",
                    entry["Nom du joueur"] + "| |"
                                             "Prénom du joueur: ", entry["Prénom du joueur"] + "| |"
                                                                                               "Âge du joueur: ",
                    entry["Âge du joueur"], "| |"
                                            "Sexe du joueur: ", entry["Sexe du joueur"] + "| |"
                                                                                          "Classement du joueur: ",
                    entry["Classement du joueur"], "| |"
                                                   "Score du joueur: ", entry["Score du joueur"], "| |")

    @staticmethod
    def creat_joueur():
        """Création du joueur."""
        joueur = []
        joueur.append(input("saisir le nom du joueur: "))
        global ljouee
        Ihm.ljouee.append(joueur)
        joueur.append(input("saisir le prénom du joueur: "))
        Ihm.ljouee.append(joueur)
        joueur.append(int(input("saisir la date de naissance du joueur: ")))
        Ihm.ljouee.append(joueur)
        joueur.append(input("saisir le genre du joueur: "))
        Ihm.ljouee.append(joueur)
        joueur.append(int(input("saisir le rang du joueur: ")))
        Ihm.ljouee.append(joueur)

        return joueur

    @staticmethod
    def saisir_joueur():
        """Création du joueur."""
        lstjoueur = []
        for i in range(1, 9):
            lstjoueur.append(int(input("saisir le n° du joueur: ")))
        print(lstjoueur)
        return lstjoueur

    # =========================                     =========================
    # ========================= TOURNOIS AFFICHAGE  =========================
    # =========================                     =========================

    @staticmethod
    def rapporttournois():
        """Rapport des tournois."""
        Ihm.mess("=========RAPPORT TOURNOIS=========")
        if not tournois_table.all():
            print('Pas de rapport ')
        else:
            print()
            print("Nom du tournois: ", "Lieu du tournois: ", "Date du tournois: ", "Id des joueurs: ",
                  "Nombre de tour: ",
                  "Contrôle de temps: ", "Description du tournois: ")
            print()
            for entry in tournois_table.all():
                print(
                    entry["nom du tournois"].ljust(17),
                    entry["lieu du tournois"].ljust(17),
                    entry["date du tournois"].ljust(20),
                    str(entry["id des joueurs"]).ljust(17),
                    str(entry["nombre de tour"]).ljust(17),
                    entry["contrôle de temps"].ljust(17),
                    entry["la description du tournois"].ljust(17)
                )

    @staticmethod
    def loadertournois():
        """Cherche les tournois avec une date de fin vide."""
        element = Query()
        nresult = []
        result = tour_table.search(element['date de fin'] == "")
        print()
        print("                         =========LIST DES TOUR EN COURS POUR CE TOURNOIS=========")
        print()
        print("Nom du tour: ".ljust(17), "Date de début du tour: ".ljust(17), "Heure de début du tour: ".ljust(17),
              "Date "
              "de "
              "fin "
              "du "
              "tour: "
              "".ljust(17),
              "Heure de fin du tour: ")
        for entry in result:
            nresult.append(entry['nom du tour'])
            print(
                entry["nom du tour"].ljust(17),
                entry["date de début"].ljust(22),
                entry["heure de début"].ljust(17),
                entry["date de fin"].ljust(17),
                entry["heure de fin"].ljust(17)
            )
        print("TOUR EN COURS POUR CE TOURNOIS: ", len(nresult))
        afaire = input("CLOTURER ?: (O/N)").lower()
        return afaire

    @staticmethod
    def creat_tournoi():
        """Summary_Création du tournois."""
        tournois = []
        global ltourn
        tournois.append(input("saisir le nom du tournois: "))
        Ihm.ltourn.append(tournois)
        tournois.append(input("saisir le lieu du tournois: "))
        Ihm.ltourn.append(tournois)
        tournois.append(input("saisir la date du tournois: "))
        Ihm.ltourn.append(tournois)
        tournois.append(int(input("saisir le nombre de tour si différent de 4: ")))
        Ihm.ltourn.append(tournois)
        tournois.append(int(input("saisir le nombre(paire) de joueurs: ")))
        Ihm.ltourn.append(tournois)
        tournois.append(input("Renseigner le contrôle de temps(bullet/blitz/coup rapide): "))
        Ihm.ltourn.append(tournois)
        tournois.append(input("saisir la description du tournois: "))
        Ihm.ltourn.append(tournois)
        return tournois

    @staticmethod
    def reponses_terminer():
        """Récupération réponse."""
        reponse = input("TERMINEE ? (O/N) ").lower()
        return reponse

    # =========================                     =========================
    # =========================    MATCH AFFICHAGE  =========================
    # =========================                     =========================
    @staticmethod
    def rapportmatchs():
        """Informations sur les matchs."""
        Ihm.mess("RAPPORT SUR LES MATCHS")
        if not match_table.all():
            print('Pas de rapport')
        else:
            print()
            print("Résultat du match du joueur 1:".ljust(41), "Id du joueur1:".ljust(31), "Résultat du match du joueur "
                                                                                          "2:".ljust(41),
                  "Id du joueur2:".ljust(41), "Id du tour:".ljust(17))
            print()
            for entry in match_table.all():
                print(entry["resultat du match Joueur 1"].ljust(31),
                      str(entry["id du joueur1"]).ljust(51),
                      entry["resultat du match Joueur 2"].ljust(21),
                      str(entry["id du joueur2"]).ljust(51),
                      str(entry["id tournois"]).ljust(31)
                      )

    @staticmethod
    def saisirmatchresultat():
        """Saisir les résultats des matches."""
        matchres = []
        for i in range(0, 4):
            matchres.append(input(f"saisir le résultat du match{i + 1} pour le joueur N°1 P pour PERDU, G pour "
                                  f"GAGNER, N pour NULL").lower())
        return matchres

    # =========================                     =========================
    # =========================    TOUR AFFICHAGE   =========================
    # =========================                     =========================

    @staticmethod
    def rapporttours():
        """Rapport des tours."""
        Ihm.mess("RAPPORT SUR LES TOURS")
        if not tour_table.all():
            print('Pas de rapport ')
        else:
            print()
            print("Nom du tour: ", "Date de début: ".ljust(30), "Heure de début: ".ljust(17), "Date de fin: ".ljust(17),
                  "Heure de fin: ".ljust(17), "Id du "
                                              "tournois "
                                              "associé:")
            print()
            for entry in tour_table.all():
                print(
                    entry["nom du tour"].ljust(17),
                    entry["date de début"].ljust(27),
                    entry["heure de début"].ljust(17),
                    entry["date de fin"].ljust(17),
                    entry["heure de fin"].ljust(17),
                    str(entry["id tournois"]).ljust(17)
                )

    @staticmethod
    def affichage_principal():
        """Affichage du menu."""
        print("=" * 32)
        print("======MENU PRINCIPAL============")
        print("================================\n")
        print("".join(Ihm.lstmenu))
        print("=" * 32)
        print("=" * 32)

    @staticmethod
    def saisie_user():
        """Secupération du choix de l'utilisateur."""
        choix = ""
        while choix == "":
            Ihm.affichage_principal()
            choix = int(input('Entrer le N° du menu & valider par ENTRER:'))
        return choix


if __name__ == "__main__":
    # t = Ihm.creat_tournoi()
    # print(t)
    # Ihm.creation_joueurs()
    # Ihm.saisie_user()
    Ihm.saisir_joueur()
