# Notes personnelles - préparation de la soutenance

Document de travail personnel, à garder hors de l'archive à rendre.
Le rapport destiné à l'enseignant est `RAPPORT.md`.

## Points à savoir expliquer à la soutenance

- **Pourquoi 69,999 et 70 ?** Ce sont les deux valeurs de part et d'autre
  du début de gratuité, au pas d'un millime. Tester seulement 100 ne révèle pas
  l'erreur au seuil.
- **Pourquoi attendre 43 DT à 200 DT ?** L'adhérent reçoit 40 DT, auxquels
  s'ajoutent 3 DT avec le code valide. Les deux avantages se cumulent.
- **Pourquoi conserver des tests rouges ?** Ils montrent que le module ne
  respecte pas la spécification ; changer les attendus cacherait les défauts.
- **Pourquoi 100 % de couverture malgré trois défauts ?** Toutes les branches
  présentes sont exécutées, mais certaines règles ne sont pas implémentées.
- **Pourquoi ne pas chercher à tuer le mutant 8 ?** Les deux conditions sont
  équivalentes sur les codes prévus par la spécification.
- **Pourquoi tester 1,5 en plus de 0 et 21 ?** Les bornes ne vérifient pas à
  elles seules l'obligation d'une quantité entière.

## Repères du chapitre 7

- **Défaut et défaillance (page 10)** : le `>` au lieu de `>=` est le défaut ;
  facturer 6 DT à un client ayant un total de 70 DT est la défaillance observée.
  La raison humaine à l'origine du défaut n'est pas connue.
- **Test et débogage (page 7)** : les tests révèlent les anomalies. Le débogage
  en cherche et corrige les causes. Dans ce projet, le module reste inchangé.
- **Oracle (page 17)** : la spécification permet de calculer le résultat
  attendu, indépendamment du résultat renvoyé par le code testé.
- **Limites du test (page 21)** : une suite réussie ou une couverture de
  100 % ne prouve pas l'absence de défauts.
- **Traçabilité (page 29)** : savoir relier une règle de `SPECIFICATION.md`
  à un test, à son résultat et, en cas d'échec, à une fiche de défaut.

## Rappels avant la remise et la soutenance

- Compléter la date de remise en tête de `RAPPORT.md` avec la date réelle.
- Relire et s'approprier les tests et le rapport. Chaque membre doit pouvoir
  expliquer n'importe quel test du groupe, son attendu et la technique utilisée.
- Savoir expliquer la vérification de couverture ajoutée au journal : les
  deux tests initiaux couvrent 8/18 branches, soit 44,44 %. Les 58 % de `Cover`
  combinent lignes et branches. La réexécution confirme ces chiffres.
- L'ancienne version du rapport distinguait déjà ces taux : aucune trace ne
  confirme que l'IA les avait confondus. Cet exemple est une vérification,
  pas une erreur de l'IA constatée. Pour satisfaire la demande du README
  d'une erreur réellement détectée et corrigée, retrouver un échange qui en
  montre une ; l'erreur de commande Python reste documentée dans l'ancien
  journal, mais elle ne concerne pas l'application du cours.
- Conserver le journal d'usage de l'IA dans le rapport : il fait partie du rendu
  demandé dans le README.
- Préparer une archive avec la dernière version du rapport et les tests,
  en excluant ce fichier personnel. L'archive déjà présente n'est pas mise à jour
  automatiquement lorsqu'un fichier Markdown change.

## Commandes sur la machine utilisée

Lors des mesures, `python` n'était pas dans le PATH. Depuis le dossier du projet,
l'interpréteur utilisé était `.\myvenv\Scripts\python.exe` :

```powershell
.\myvenv\Scripts\python.exe -m pytest
.\myvenv\Scripts\python.exe -m pytest --cov=panier --cov-branch --cov-report=term-missing
.\myvenv\Scripts\python.exe verifier_mutants.py
```

La suite documentée compte 84 cas : 77 réussites et 7 échecs correspondant
à trois défauts. Le code de sortie 1 de pytest est donc attendu ici.
Les sept échecs doivent rester visibles, sans `skip` ni `xfail`.

Pendant l'assistance, l'accès à l'interpréteur Python a également nécessité
une autorisation d'exécution hors du bac à sable de l'outil.
