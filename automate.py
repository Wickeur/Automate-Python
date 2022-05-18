# Réaliser par Julian Wicke, Simon , Quentin et Enzo
import pydot

graph = pydot.Dot(graph_type='digraph')

fichierTXT = open("texte.txt", "r")
fichierWrite = open("texte.txt", "a")

entrees = []
sorties = []
etats = []
alphabet = []
transitions = []

automate = {
    "entrees": entrees,
    "sorties": sorties,
    "etats": etats,
    "alphabet": alphabet,
    "transitions": transitions,
}

etatInit = ""
action = ""
etatFinal = ""
intNum = 0


numeroLigne = 0

chaine = ""

# Afficher tout les infos de l'automate
for x in fichierTXT:
    for y in x:
        # Detecte la fin d'une ligne
        if y == ";":
            if numeroLigne > 3:
                if intNum == 2:
                    etatFinal = chaine
                    chaine = ""

                chemin = {
                    "etat_initiale": etatInit,
                    "action": action,
                    "etat_finale": etatFinal,
                }

                transitions.append(chemin)

                intNum = 0
                etatInit = ""
                action = ""
                etatFinal = ""

            numeroLigne += 1

        # Stocke les entrees
        elif numeroLigne == 0:
            if y == "-" and chaine != "":
                entrees.append(chaine)
                chaine = ""
            elif y != " " and y != '\n':
                chaine += y

        # Stocke les sorties
        elif numeroLigne == 1:
            if y == "*" and chaine != "":
                sorties.append(chaine)
                chaine = ""
            elif y != " " and y != '\n':
                chaine += y

        # Stocke les etats
        elif numeroLigne == 2:
            if y == "E" and chaine != "":
                etats.append(chaine)
                chaine = ""
            elif y != " " and y != '\n':
                chaine += y

        # Stocke les alphabet
        elif numeroLigne == 3:
            if y == "A" and chaine != "":
                alphabet.append(chaine)
                chaine = ""
            elif y != " " and y != '\n':
                chaine += y

        # Stocke les changements transitions
        elif numeroLigne > 3:
            if y == ">" and chaine != "":
                if intNum == 0:
                    etatInit = chaine
                elif intNum == 1:
                    action = chaine
                chaine = ""
                intNum += 1
            elif y != " " and y != '\n':
                chaine += y

# affichage de l'automate
print("Les entrées sont", automate["entrees"],
      "Les sorties sont", automate["sorties"],
      "Les états sont", automate["etats"],
      "L'alphabet sont", automate["alphabet"],
      "Les chemins sont", automate["transitions"])


def dessinerGraph(nom):
    # Pour l'entrée
    for j in range(len(automate["entrees"])):
        e = automate["entrees"][j]  # initialise
        entrée = pydot.Node("Entrée", style="filled",
                            fillcolor="green")  # creer une bulle entrée
        graph.add_node(entrée)  # ajouter la bulle
        graph.add_edge(pydot.Edge(entrée,  e))  # il créer le chemin d'entrée

    # Pour les liens
    for i in range(len(automate["transitions"])):

        a = automate["transitions"][i]["etat_initiale"]
        b = automate["transitions"][i]["action"]
        c = automate["transitions"][i]["etat_finale"]

        graph.add_edge(pydot.Edge(a, c, label=b, fontsize="10"))

    # Pour la sorties
    for m in range(len(automate["entrees"])):
        s = automate["sorties"][m]
        sorties = pydot.Node("sorties", style="filled", fillcolor="red")
        graph.add_node(sorties)
        graph.add_edge(pydot.Edge(s, sorties))

    graph.write_png(nom)


dessinerGraph("automate.png")


# Donne l'accessibilité de l'état envoyer

def TestAccessibilite(etat):
    etatAccessible = []
    etatTester = []
    boucle = True

    while boucle:

        for i in range(len(etatTester)):

            if etatTester[i] == etat:
                boucle = False

                for j in range(len(etatAccessible)):
                    add = True

                    for k in range(len(etatTester)):
                        if etatAccessible[j] == etatTester[k]:
                            add = False

                    if add == True:
                        etat = etatAccessible[j]
                        boucle = True

        etatTester.append(etat)
        for i in range(len(automate["transitions"])):

            if automate["transitions"][i]["etat_initiale"] == etat:
                canAdd = True

                for j in range(len(etatAccessible)):

                    if etatAccessible[j] == automate["transitions"][i]["etat_finale"]:
                        canAdd = False

                if canAdd == True:
                    etatAccessible.append(
                        automate["transitions"][i]["etat_finale"])

    return etatAccessible


etatAccessible = []
etatAccessible = TestAccessibilite(automate["entrees"][0])
print("Les etats Accessibles sont :", etatAccessible)


# Regarde si l'état envoyer et CoAccessible

etatCoAccessible = []


def TestCoAccessibilite(etat):
    etatAcc = []
    etatAcc = TestAccessibilite(etat)
    for i in range(len(etatAcc)):
        for j in range(len(automate["sorties"])):

            if etatAcc[i] == automate["sorties"][j]:
                etatCoAccessible.append(etat)
                return


for i in range(len(automate["etats"])):
    TestCoAccessibilite(automate["etats"][i])

print("Les etats Co-Accessible sont :", etatCoAccessible)


def CompletionEtat():
    for i in range(len(automate["etats"])):
        # Remplire une liste avec tout les états sauf soi même
        monAlphabet = automate["alphabet"]

        alphabetAccessible = []
        for j in range(len(automate["transitions"])):
            if automate["transitions"][j]["etat_initiale"] == automate["etats"][i]:
                alphabetAccessible.append(automate["transitions"][j]["action"])

        alphabetNonAccessible = []
        for k in range(len(monAlphabet)):
            if not (monAlphabet[k] in alphabetAccessible):
                alphabetNonAccessible.append(monAlphabet[k])

        for l in range(len(alphabetNonAccessible)):
            ligne = '\n' + automate["etats"][i] + \
                " > " + alphabetNonAccessible[l] + " > P;"

            fichierWrite.write(ligne)


CompletionEtat()


def determinerAutomate(element):
    etatTransitionIdentique = []

    for i in range(len(automate["transition"])):
        if (automate["transition"][i]["etat_initiale"] == element and automate["transition"][i]["etat_final"] == automate["alphabet"]):
            etatTransitionIdentique.append(i)

# determinerAutomate()


dessinerGraph("automate2.png")

fichierTXT.close()
