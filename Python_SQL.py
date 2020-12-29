import sqlite3
conn=sqlite3.connect('student.sqlite')
cur=conn.cursor()
#_____Question 1_____________________________:
def insBU(nomE):
	#requête pour selectionner les étudiants dont leur nom égale à nomE 
    cur.execute("select nomE from Etudiant where nomE=?",(nomE,))
    #afficher tous les tuples dans une liste qui vérifient la condition au dessus
    liste=cur.fetchall()
    #si la liste est vide c-à-d le nom écrit par l'utilisateur n'appartient pas  à notre table
    if liste==[]:
          print("Ce nom n’existe pas dans la base")
    #sinon s'il est dans notre table voilà la requête pour afficher sa date d'inscription 
    else:
      cur.execute("select dateInscripBU from etudiant where nomE=:nomE",{'nomE':nomE})
      #une boucle pour afficher le resultat ou bien faire print(cur.fetchall)'mode d'affichage'
      for k in cur:
            print(k)
#Donner le droit au utilisateur d'entrer le nom de l'étudiant  souhaiter            
nom=input("Entrer le nom :")
insBU(nom)
#_____Question 2_____________________________:
def insCour(num_cours):
#requête pour selectionner les étudiants inscrits dont leur numéro de cours égale à num_cours
      cur.execute("""select nomE,prenomE from etudiant,Inscrit 
                  where etudiant.num_etu=Inscrit.NumEtudiant 
                 and num_cours={}""".format(num_cours))
      #Boucle pour afficher le résultat, ou bien print(cur.fetchall)
      for k in cur:
            print(k)
#Donner le droit au utilisateur d'entrer le numéro  de cours  souhaiter 
numC=int(input("Entrer le numéro :"))
insCour(numC)
#_____Question 3_____________________________:
def ResuEtu(num_etu):
            a=cur.execute("""select nomE,prenomE,note,nomc
                from Etudiant,Resultat,Cours
                where Resultat.num_etu=Etudiant.num_etu
                and Resultat.num_cours=Cours.num_cours
                and Etudiant.num_etu={}""".format(num_etu))
            print(a.fetchall())
            b=cur.execute("""select num_cours from resultat where num_etu={}""".format(num_etu))
            #convertire le resultat de la requête au dessus en liste 
            c=list(b)
            #boucle pour parcourir la liste (longueur de la liste) 
            #len:une fonction qui retourne la longueur d'une liste
            for i in range(len(c)):
            #requête pour selectionner max(note) et min et avg de chaque cours de l'etudiant choisi par l'utilisateur  
                cur.execute("""select max(note),min(note),AVG(note),num_cours from Resultat 
                where num_cours=?""",(c[i][0],))
                print(cur.fetchone())
            #requête pour selectionner la moyenne générale de l'etudiant choisi par l'utilisateur
            cur.execute("""select AVG(note) from Resultat 
                                where num_etu={}""".format(num_etu))
            print(cur.fetchone())
#Donner le droit au utilisateur d'entrer le numéro de l'étudiant  souhaiter 
num_etu = int(input("Entrer le numéro de l'étudiant : "))
ResuEtu(num_etu)
#_____Question 4_____________________________:
def ResultEchec():
    cur.execute("""select avg(note),nomC,numclass 
                    from resultat r,cours c, class cl , etudiant e
                    where c.num_cours=r.num_cours and  cl.numClass=e.numClasse 
                    and e.num_etu=r.num_etu group by nomclass,nomc""")
    for k in cur:
        print(k)
    req=cur.execute("""select  nomE,prenomE,note,nomc ,r.num_etu,r.num_cours,numclasse
                from etudiant e, resultat r, cours c
                where e.num_etu=r.num_etu 
                and c.num_cours=r.num_cours 
                and note<10
                group by nomc,nomE""")
    for i in req:
        print(i)
ResultEchec()
#_____Question 5_____________________________:
def insr():
#requête pour selectionner les étudiants inscrits dans tous les cours c-à-d leurs numéros est répétés 8 fois dans la table inscrit (dans notre cas on a 8 cours) 
    cur.execute("""select nomE,num_etu from etudiant 
    where (select count(numEtudiant) from inscrit  where inscrit.numEtudiant=etudiant.num_etu)=(select count(*) from cours)""")
    print(cur.fetchall())

insr()
#_____Question 6_____________________________:
def empLiv(Nlivre):
    cur.execute("""select nomE,dateRetour from etudiant e,pret p
    where e.num_etu=p.num_etu and Nlivre={}""".format(Nlivre))
    print(cur.fetchall())
#Donner le droit au utilisateur d'entrer le numéro de livre souhaiter 
NumLiv= int(input("Entrer le numéro de livre : "))
empLiv(NumLiv)
#_____Question 7_____________________________:
def retard():
    cur.execute("""select nomE,dateRetour,dateretourPrevue from etudiant e,pret p
    where e.num_etu=p.num_etu and dateretour>dateretourPrevue""")
    for i in cur:
      print(i)
retard()
#_____Question 8_____________________________:
def noEmp():
    cur.execute("""select nomE,titre from Livre l,pret p,etudiant e
    where l.Nlivre=p.Nlivre  and e.num_etu=p.num_etu
    group by nomE,titre""")
    for i in cur:
        print(i)
noEmp()
#_____Question 9_____________________________:
def ResultTot():
    cur.execute("""select  nomclass,nomc,avg(note) 
                 from class cl,cours c,etudiant e,resultat r
                 where e.numclasse=cl.numclass and r.num_etu=e.num_etu 
                 and c.num_cours=r.num_cours 
                 group by nomclass,nomc""")
    for i in cur:
        print(i)
ResultTot()
#_____Question 10_____________________________:
cur.execute("""select nomP,nomc from  enseignant e,cours c 
             where  c.num_ens=e.num_ens""")
for i in cur:
    print(i)
#_____Question [Q1]_____________________________:
def updateCours(num_Cours):
	#Donner le droit au utilisateur d'entrer le nouveau nom de cours  souhaiter
    newNom= input("Enter le nouveau nom du cours  numéro "+str(num_Cours)+" : " )
    #requête pour modifier le cours  
    cur.execute("""UPDATE Cours SET nomC=? where num_cours=?""",(newNom,num_Cours,))
    a=cur.execute("""select  num_cours,nomC from Cours where num_cours=?""",(num_Cours,))
    print("Le nouveau  cours numéro :",a.fetchone())
#Donner le droit au utilisateur d'entrer le numéro de cours souhaiter 
numC=int(input("Entrer le numéro de cours:"))
updateCours(numC)
#_____Question [Q2]_____________________________:
def DeleteCours(num_cours):
	#requête pour supprimer  le cours dont le numéro égale à num_cours 
    cur.execute("""Delete From Cours where num_cours=?""",(num_cours,))
    print("Le Cours numéro "+str(num_cours)+" est bien supprimé .")

#Donner le droit au utilisateur d'entrer le numéro de cours  souhaiter 
numC=int(input("Entrer le numéro de Cours : "))
DeleteCours(numC)
#_____Camembert_____________________________:
import matplotlib.pyplot as plt
import sqlite3
conn=sqlite3.connect('student.sqlite')
cur=conn.cursor()
labels = 'note>=14','note<8','12=<note<14','8<note<=10','10<note<12'
sizes = []
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','pink']
 #requête pour selectionner la moyenne générale de chaque étudiant dans la table résultat 
cur.execute("""select avg(note) from resultat group by num_etu""")
c=list(cur)
#déclaration d'une liste vide 
liste=[]
for i in range(len(c)):
    liste.append(c[i][0])
#les compteurs 
a=0
b=0
d=0
E=0
F=0
#boucle pour obtenir les 'sizes'
for k in range(len(c)):
    if liste[k]<8 or liste[k]==8:
        a+=1
    elif liste[k]>14 or liste[k]==14:
        b+=1
    elif 10 > liste[k] > 8 or liste[k] == 10:
        d+=1
    elif 14 > liste[k] > 12 or liste[k] == 12 :
        E+=1
    else :
        F+=1
#pour remplire la liste sizes=[] 
sizes.append(b)
sizes.append(a)
sizes.append(E)
sizes.append(d)
sizes.append(F)
explode=(0,0,0.1,0,0)
plt.pie(sizes, labels=labels ,colors=colors,explode=explode,
        autopct='%1.1f%%', shadow=True, startangle=90)

plt.axis('equal')
plt.title('Répartition de notes par moyenne ')
plt.show()
#_____Histogramme_____________________________:
import matplotlib.pyplot as plt
import sqlite3
conn=sqlite3.connect('student.sqlite')
cur=conn.cursor()
cur.execute("""select avg(note) from resultat group by num_etu""")
c=list(cur)
liste=[]
for i in range(len(c)):
    liste.append(c[i][0])
#la fonction set pour supprimer les duplicates dans la liste 
tab=list(set(liste))
hauteurs_barres = []
for k in range(len(tab)):
    a=liste.count(tab[k])
    hauteurs_barres.append(a)
largeur_barres = 0.1
plt.bar(tab, hauteurs_barres, largeur_barres,color='yellowgreen')
plt.title("Histogramme")
plt.xlabel("Note")
plt.ylabel("Nombre d'élèves")
plt.show()
#FIN_____________________________.
conn.commit()
conn.close()