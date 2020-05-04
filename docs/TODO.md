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
    - [-] Orang



###	API WEB INTERFACE

-  [-] Rechargement d'une carte monnamon
-  [-] Reporting
