#Partie 1
def hanoi(n , depart, milieu, arrivee):
    if n==1:
        # C'est la condition d'arret, si on a seulement 1 seul disque sur la tour 1 on le deplace directement vers la tour 2. 
        print ("Deplacer disque 1 de la "+depart+" vers " + milieu)
        return # Pour arreter le code car c'est le dernier disque a deplacer. 
    hanoi(n-1, depart, arrivee, milieu) # On envoie les n-1 premiers disques sur la place du milieu donc c'est un appel recursive avec le depart a gauche et l'arrivee au milieu
    print ("Deplacer disque " + str(n) +" de la "+depart+" vers " + milieu)
    hanoi(n-1, arrivee, milieu, depart) #  Dans ce cas on envois les n-1 premiers disques sur la droite donc on a le depart au milieu et l'arrivee a droite
       
#Partie 2
hanoi(3,'tour1','tour2','tour3')
#Pour n = 6 on a 63 deplacements
# Pour n quelconque on a 2^n - 1 ; Pour le cas de n=6 on avais 2^6 + 1 = 63 etapes.