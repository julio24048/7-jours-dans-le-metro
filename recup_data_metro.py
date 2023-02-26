#import des modules
from requests.auth import HTTPBasicAuth
import pandas as pd
import requests
import json
from datetime import datetime
from time import strftime
import time

#initialisation du dataframe
df = pd.DataFrame({'timecode': [],'ligne':[],'statut':[]})

#initialisation de la liste contenant les codes des lignes de métro pour alimenter la boucle de la fonction en dessous
codes_lignes = ['C01371','C01372','C01373','C01374','C01375','C01376','C01377',
               'C01378','C01379','C01380','C01381','C01382','C01383','C01384']

#fonction de requetage sur les lignes de métro
def requete_lignes () :
    #déclaration du dataframe comme variable globale
    global df
    #boucle sur l'ensemble des lignes
    for i in range(len(codes_lignes)) :  
        #envoi de la requete et traitement du retour
        try : 
            url = 'https://prim.iledefrance-mobilites.fr/marketplace/general-message?LineRef=STIF%3ALine%3A%3A'+codes_lignes[i]+'%3A&InfoChannelRef=Perturbation'
            headers = {'Accept': 'application/json','apikey': 'YLqkwzUeMRT43lUTWaDIKP41LZAG7eAx'}
            req = requests.get(url, headers=headers)
            #si tout se passe bien on traite les résultats
            if (req.status_code == 200) :
                #conversion sous forme de dictionnaire des données
                contenu = req.content.decode("utf-8")
                dico = json.loads(contenu)
                #on récupère les messages et on les ajoute au dataframe 
                if len(dico["Siri"]["ServiceDelivery"]["GeneralMessageDelivery"][0]['InfoMessage']) > 0 :
                    for j in range(len(dico["Siri"]["ServiceDelivery"]["GeneralMessageDelivery"][0]['InfoMessage'])) :
                        tmp = pd.DataFrame({'timecode': [datetime.now()], 'ligne': [i+1],
                        'statut':[dico["Siri"]["ServiceDelivery"]["GeneralMessageDelivery"][0]['InfoMessage'][j]['Content']['Message'][0]['MessageText']['value']]})
                        df = pd.concat([df, tmp], axis = 0)

                else :
                    tmp = pd.DataFrame({'timecode': [datetime.now()], 'ligne': [i+1],'statut': ['tout va bien']})
                    df = pd.concat([df, tmp], axis = 0)
            #on attend 2 secondes avant de lancer une autre requete
            time.sleep(2)
        #si on a un problème de connexion, prise en charge de l'erreur  
        except requests.exceptions.ConnectionError :
            print('problème de connexion : ' + str(datetime.now()))
    #export du cvs journalisé
    maintenant = datetime.now()
    df.to_csv('journal'+maintenant.strftime("%d%m%Y")+'.csv')
    

#indication de l'heure de lancement
print('heure de lancement : ' + str(datetime.now()))

#création d'une variable fictive pour une boucle infinie
infiniteloop = True
while infiniteloop == True :
    #lancement du requetage tous les quart d'heures seulement aux heures où le métro circule
    if int(datetime.now().strftime("%H")) in [0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] :
        requete_lignes ()
    time.sleep(872)