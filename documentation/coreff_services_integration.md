Présentation des services à intégrer à la plateforme InfiBail
=============================================================

#Societe.com

##Présentation générale
Dans MyPortal, le service societe.com permet aujourd'hui de compléter les fiches société. 

Les Web Services de societe.com permettent : 
* d'identifier une entreprise à partir de son Siren, de sa raison sociale, de ses dirigeants, de son adresse, de son code activité (établissements inclus).
* d'accéder à la fiche identité détaillée de l’entreprise.

Les informations disponibles sont :

* Informations juridiques :  
	* Siren/siret (identifiant légal unique à 9 chiffres)  
	* Nature de l'établissementt  
	* Raison social  
	* Nom commercial  
	* Enseigne  
	* Adresse  
	* CP  
	* Commune  
	* Code NAF  
	* Libellé activité  
	* Date d'immatriculation  
	* Forme juridique  
	* Capital social  
	* Nom du dirigeant  
	* Fonction du dirigeant  
	* Date de naissance  
	
* Informations financières et chiffres clés :  
	* Chiffre d'affaires  
	* Résultat net  
	* Date de clôture  
	* Unité monétaire  
	* Effectif   
	
* Evènements :  
	* Dernier évènement dépôt légal  
	* Date de l'évènement  
	* Dernier jugement (procédures collectives)  
	* Date du jugement  
	* Radiation  

##Présentation technique
La récupération de toutes les informations liées à une société se fait via un simple appel HTTPS 

```
https://api.societe.com/cgi-bin/detxml?user=***&pass=***&siren=33480569400034
```

Plusieurs codes erreurs possibles en cas de problème : 

1. Erreur dans les arguments passés
2. Accès refusé
3. Fréquence trop élevée
4. Pb de paramètres
5. Pas de réponse
6. Problème de communication avec le serveur societe.com

Sinon, si tout se passe bien, un flux XML est retourné dans le réponse HTTP.

  
Une documentation complète est disponible dans NextCloud à l'emplacement suivant : nextCloud/InfiBail/Architecture/Servcies/Societe.com/API Pro Societe.com.pdf

##Interlocuteurs
* Cyrille Valayan cvalayan@societe.com


#CreditSafe

##Présentation générale 
CreditSafe est un service en ligne permettant d'obtenir des informations sur une société, ses dirigeants, mais également toutes ses informations financières.
C'est un service très complet. A noter toutefois dans certains cas l'obsolescence de certaines informations.  

##Présentation technique 

Toutes les opérations possibles sont décrites dans un WSDL : 

```
https://www.creditsafe.fr/getdata/service/CSFRServices.asmx?wsdl
```


```
<xmlrequest>
	<header>
		<username>***</username>
		<password>***</password>
		<operation>companysearch|getcompanyinformation|directorsearch|getdirectorinformation</operation>
		<language>FR|EN</language>
		<country>FR</country>
		<chargereference>2018-XXXX</chargereference>
	</header>
	<body>
		<package></package>		
		<companynumber></companynumber>		
		<name></name>
		<namesearchmode>begin</namesearchmode> 
		<address></address>
		<addresssearchmode>begin</addresssearchmode> 
		<postcode></postcode> 
		<telephone></telephone>
		<startposition>1</startposition>
		<pagesize>25</pagesize>
	</body>
</xmlrequest>
```

Une documentation complète est disponible dans NextCloud à l'emplacement suivant : nextCloud/InfiBail/Architecture/Servcies/CreditSafe/CSFR_GetData_v1.0-Guide_utilisateur.pdf


##Interlocuteurs
M Mathieu Lannoy
06 30 45 58 55
Mathieu.Lannoy@creditsafe.fr

MME Aya AL FARTOUSSI 
Ligne Directe : +33 (0) 3 20 69 11 97 | Mobile : +33 (0) 6 13 74 36 12
Aya.AlFartoussi@creditsafe.fr

