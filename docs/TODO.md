## Tout sur les APIs

### TODO

Les changements à apporter, les bonnes idées ou encore les dettes techniques font parti de 
ce fichier. Il faudra les supprimer au fur et à mesure qu'ils ont été faits et testés. 

* `[x] Demander lors de l'envoi la date de délivrance et d'expiration de la pièce d'identitté du client`

* [-] Avant de créditer ou de débiter s'assure que l'opération se fasse dans la devise appropriée

* [x]  Revoir validateur CashToCashValidator : Accepter que certains champs ne soient pas remplis
    - `[x] partial = True`

* [x]  Réponses API
    - `[x] Renvoyer les réponses de type : `{response_code : 'XXX', response_text: 'YYYYY'}` pour toutes les APIs`
    - `[x] S'assurer que le code succès soit : {response_code : '000', response_text: 'YYYYY'}`

* [x] Finir les intégrations des partenaires à partir de `payer_network` 
    - [-] World Remit 
    - [-] Small World 
    - [-] Orange money 

* [x] Les types de transactions à faire
    - `[x] Cash to Cash` 
    - [-]  Cash to Cash en prenant en compte le réseau payeur
    - `[x] Activation Carte` 
    - `[x] Retrait Cash` 
    - [-]  Rechargement carte monnamon
    - `[x] Rechargement compte Wallet`
    - `[x] Rechargement compte entité` 
    - [-] Retrait compte entité

    
### API CARTERA

Cartera est une application mobile qui permet aux utilisateurs de MONAMON de faire tout un ensemble de services 
financiers avec leur téléphone portable allant du transfert d’argent au paiement de la scolarité de leurs enfants. 

- [-] Envoyer de l’argent
- [-] Carte MONAMON 
    - [-] Solde, historique de la carte
    - [-] Historique des transactions
- [-] Payer avec Cartera : Scanner un QR code ; entrer le numero du marchand…
- [-] 	Retirer de l’argent : Numero du POS puis valider avec une OPT
- [-] Payer une facture : Electricite, Eau, Scolarité etc…
- [-] Achat de crédit : Orange, MTN
- [-] Historique


###	API WEB INTERFACE

- [-] Tableau de bord
    - [-] Solde entité
    - [-] Montant encaissé au jour J
    - [-] Montant décaissé au jour J
    - [-] Commission gagnée au jour J

- `[x] Transfert cash to cash`
- `[x] Activation de carte de monnamon`
-  [-] Rechargement d'une carte monnamon
- `[-] Transfert d'argent cash to Wallet`
-  [-] Paiement marchand
-  [-] Reporting
- `[x] Calculateur de frais`
