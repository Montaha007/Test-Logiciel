# Rapport de test - groupe 05

Membres : **à compléter (trois noms)**. Date de remise : **à compléter**.

Mesures réalisées le 15 novembre 2026, sous Windows, avec Python 3.14.8,
pytest 9.2.0, pytest-cov 7.1.0 et coverage.py 7.17.3.

Le module est testé selon `SPECIFICATION.md`. Les valeurs du groupe sont :
quantités de 1 à 20, remise adhérent de 20 % dès 150 DT, code `LISTE3`
donnant 3 DT, livraison gratuite dès 70 DT et tarifs de 6 ou 9 DT.
Les exemples des diapositives utilisent parfois d'autres seuils : ils servent
pour la méthode, pas pour les résultats attendus de ce projet.

La suite contient **84 cas : 77 réussites et 7 échecs**, correspondant à
**trois défauts**. Les tests en échec restent actifs, sans `skip` ni `xfail`.
`panier.py`, les mutants et `verifier_mutants.py` n'ont pas été modifiés.

## Tâche 1 - Partitions et valeurs limites

### 1.a Partitions de `frais_livraison`

Le découpage se fait par paramètre. Les partitions d'un même paramètre sont
disjointes ; un test peut couvrir une partition de chaque paramètre à la fois.
Pour un cas invalide, les autres entrées restent valides afin de ne pas masquer
le contrôle recherché (chapitre 8, pages 8 à 12).

| N° | Paramètre et partition | Valide ? | Appel représentatif | Résultat attendu | Test |
|---|---|---|---|---|---|
| P1 | Total < 0 | Non | `(-0.001, "GRAND_TUNIS", False)` | `ValueError` | `test_frais_total_negatif_refuse` |
| P2 | 0 ≤ total < 70 | Oui | `(25, "GRAND_TUNIS", False)` | 6,000 DT | `test_frais_payants_sous_seuil` |
| P3 | Total ≥ 70 | Oui | `(100, "INTERIEUR", False)` | 0,000 DT | `test_frais_gratuits_au_dessus_du_seuil` |
| P4 | Zone Grand Tunis | Oui | `(10, "GRAND_TUNIS", False)` | 6,000 DT | `test_frais_grand_tunis` |
| P5 | Zone intérieur | Oui | `(25, "INTERIEUR", False)` | 9,000 DT | `test_frais_payants_sous_seuil` |
| P6 | Toute autre zone | Non | `(10, "SFAX", False)` | `ValueError` | `test_frais_zone_invalide_meme_si_gratuite` |
| P7 | Client standard | Oui | `(25, "INTERIEUR", False)` | 9,000 DT | `test_frais_payants_sous_seuil` |
| P8 | Client Premium | Oui | `(10, "INTERIEUR", True)` | 0,000 DT | `test_frais_premium_gratuits` |

Les huit partitions sont exercées : **8/8**. Cela ne signifie pas que toutes
leurs combinaisons ont été testées.

Des croisements utiles complètent ces représentants : zone inconnue, en
minuscules, vide ou absente, avec et sans Premium, sous et au-dessus du seuil.
Une zone invalide doit toujours lever `ValueError`, même si la livraison aurait
été gratuite. Le total négatif est aussi testé avec Premium dans les deux
zones. Aucun comportement n'est inventé pour un total non numérique, non décrit
dans la spécification.

### 1.b Valeurs limites de `frais_livraison` (analyse à 2 valeurs)

Le pas retenu est **0,001 DT**, soit un millime. Pour chaque frontière, on prend
la limite et sa voisine dans la partition adjacente (chapitre 8, pages 21 à 26).

| Frontière | Valeurs testées | Contexte | Résultats attendus | Tests |
|---|---|---|---|---|
| Début des totaux valides | -0,001 ; 0,000 | Standard, Grand Tunis | `ValueError` ; 6,000 DT | `test_frais_total_negatif_refuse`, `test_frais_payants_sous_seuil` |
| Début des totaux valides | -0,001 ; 0,000 | Standard, intérieur | `ValueError` ; 9,000 DT | Mêmes tests, autre zone |
| Début de la gratuité | 69,999 ; 70,000 | Standard, Grand Tunis | 6,000 ; 0,000 DT | `test_frais_payants_sous_seuil`, `test_frais_gratuits_au_seuil` |
| Début de la gratuité | 69,999 ; 70,000 | Standard, intérieur | 9,000 ; 0,000 DT | Mêmes tests, autre zone |

Les quatre valeurs distinctes retenues sont exercées : **4/4**. Les cas à
70,001 et 100 DT sont des compléments ; ils ne remplacent pas 70,000 DT.
Les zones sont des catégories, sans limites numériques. Aucune limite
supérieure du total n'est spécifiée.

### 1.c Valeurs limites et boucle de `total_panier`

| Élément | Données testées | Résultats attendus | Tests |
|---|---|---|---|
| Quantité : limite basse | Prix 2 DT, quantités 0 et 1 | `ValueError` ; 2,000 DT | `test_total_quantite_hors_bornes`, `test_total_quantite_aux_bornes_valides` |
| Quantité : limite haute | Prix 2 DT, quantités 20 et 21 | 40,000 DT ; `ValueError` | Mêmes tests |
| Quantité non entière | `[(2.0, 1.5)]` | `ValueError` | `test_total_quantite_non_entiere` |
| Prix : limite basse | Prix 0 et 0,001 DT, quantité 1 | `ValueError` ; 0,001 DT | `test_total_prix_non_positif`, `test_total_prix_un_millime` |
| Prix négatif (complément) | `[(-0.001, 1)]` | `ValueError` | `test_total_prix_non_positif[negatif]` |
| Boucle : 0 ligne | `[]` | 0,000 DT | `test_total_panier_vide` |
| Boucle : 1 ligne | `[(2.0, 3)]` | 6,000 DT | `test_total_un_article` |
| Boucle : 2 lignes | `[(2.5, 4), (1.2, 3)]` | 10 + 3,6 = 13,600 DT | `test_total_deux_lignes` |
| Validation au deuxième passage | Ligne valide puis `(0, 1)` ou `(2, 21)` | `ValueError` dans chaque cas | `test_total_verifie_aussi_la_deuxieme_ligne` |
| Arrondi du résultat | Prix 1,2344 et 1,2346 DT, quantité 1 | 1,234 et 1,235 DT | `test_total_arrondi_au_millime` |

Les quatre limites de quantité et les deux limites de prix sont couvertes.
Il n'y a pas de prix maximal ni de nombre maximal de lignes dans la
spécification : aucune borne supérieure n'est ajoutée.
Les deux cas d'arrondi utilisent des prix positifs avec une précision supérieure
au millime pour vérifier le résultat ; ils évitent les égalités à mi-chemin,
dont le mode d'arrondi n'est pas précisé.

Le test à deux lignes vérifie le cumul : il peut repérer un calcul qui ne
garderait que la dernière ligne. Le choix 0, 1 et 2 itérations vient du
chapitre 9, page 42.

## Tâche 2 - Table de décision de `remise`

Conditions : **C1** = adhérent ; **C2** = total ≥ 150 DT ; **C3** = code
exactement égal à `LISTE3`. V signifie vrai, F faux, X action appliquée,
et « - » condition sans importance. Les montants sont en DT.

### 2.a Table complète (8 colonnes)

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| C1 adhérent | V | V | V | V | F | F | F | F |
| C2 total ≥ 150 | V | V | F | F | V | V | F | F |
| C3 code valide | V | F | V | F | V | F | V | F |
| Ajouter 20 % du total | X | X | | | | | | |
| Ajouter 3 DT | X | | X | | X | | X | |
| Montant avant plafond | 0,20t + 3 | 0,20t | 3 | 0 | 3 | 0 | 3 | 0 |

Toutes les colonnes sont réalisables. Après les additions, le résultat doit
être limité au total : `min(total, montant)`, puis rendu au millime.
Le plafond est une règle supplémentaire, non une quatrième condition ajoutée
aux huit colonnes demandées.

### 2.b Table simplifiée et tests

R3 et R7 produisent les mêmes actions et ne diffèrent que par C1 : ils
fusionnent. Il en va de même pour R4 et R8. Les autres colonnes restent
séparées. Cela donne **six colonnes**, car les deux remises se cumulent.

Les six tests ci-dessous sont les paramètres de `test_remise_table_simplifiee`.

| Colonne | Origine | C1 | C2 | C3 | Données `(total, adherent, code)` | Remise attendue | Identifiant du test |
|---|---|---|---|---|---|---|---|
| S1 | R1 | V | V | V | `(200, True, "LISTE3")` | 43,000 | `S1_cumul` |
| S2 | R2 | V | V | F | `(200, True, None)` | 40,000 | `S2_adherent_seul` |
| S3 | R3 + R7 | - | F | V | `(100, True, "LISTE3")` | 3,000 | `S3_promo_sous_seuil` |
| S4 | R4 + R8 | - | F | F | `(100, True, None)` | 0,000 | `S4_aucune_sous_seuil` |
| S5 | R5 | F | V | V | `(200, False, "LISTE3")` | 3,000 | `S5_promo_non_adherent` |
| S6 | R6 | F | V | F | `(200, False, None)` | 0,000 | `S6_aucune_non_adherent` |

Couverture : **6/6 colonnes simplifiées**. Les deux cas de
`test_remise_non_adherent_sous_seuil` exercent R7 et R8 explicitement :
avec ces compléments, **8/8 colonnes complètes** sont exercées.

| Complément | Données | Attendu | Test |
|---|---|---|---|
| Seuil adhérent inclus | 149,999 puis 150 DT, adhérent, sans code | 0 puis 30 DT | `test_remise_limites_seuil_adherent` |
| Cumul au seuil | Mêmes totaux, adhérent, `LISTE3` | 3 puis 33 DT | Même test, paramètres avec promo |
| Plafond | `(2, False, "LISTE3")` et `(2, True, "LISTE3")` | 2 DT dans les deux cas | `test_remise_plafonnee_au_total` |
| Plafond, total nul et juste sous 3 | `(0, False, "LISTE3")`, `(2.999, False, "LISTE3")` | 0 et 2,999 DT | Même test |
| À 3 DT et juste après | Totaux 3 et 3,001, non-adhérent, `LISTE3` | 3 DT | `test_remise_code_au_plafond_et_apres` |
| Code absent, panier nul | Total 0, avec et sans adhésion | 0 DT | `test_remise_total_nul_sans_code` |
| Code différent | `liste3`, `Liste3`, espaces, chaîne vide, `AUTRE`, adhérent à 200 DT | 40 DT : la remise adhérent reste due | `test_remise_code_different_ignore` |
| Arrondi | Adhérent à 150,002 puis 150,003 DT | 30,000 puis 30,001 DT | `test_remise_arrondie_au_millime` |

Les attendus sont écrits dans les paramètres des tests. Ils ne sont pas
obtenus en appelant le module et les constantes du module ne servent pas
d'oracle. Les nouveaux tests numériques utilisent une tolérance absolue de
`1e-9`, sans tolérance relative : elle est bien inférieure à un millime.

## Tâche 3 - Couverture des branches

Les deux tests fournis au départ ont été conservés. La mesure initiale a
été faite avant l'ajout de la suite, puis reproduite en sélectionnant seulement
ces deux fonctions. Les sorties et JSON sont dans `resultats/`.

| Mesure | Couverture des branches | Lignes couvertes | Branches non couvertes |
|---|---|---|---|
| Deux tests de départ | **8/18 = 44,44 %** | 23/35 = 65,71 % | 10 arcs, détaillés ci-dessous |
| Suite finale, 84 cas | **18/18 = 100 %** | 35/35 = 100 % | Aucune |

Arcs manquants au départ, avec les numéros de lignes de `panier.py` :

| Fonction | Arcs manquants | Ce qui manquait |
|---|---|---|
| `total_panier` | 22→23, 24→25 | Refus du prix et de la quantité |
| `remise` | 33→34, 33→35, 35→36, 35→37 | Les deux issues de chacune des deux décisions |
| `frais_livraison` | 42→43, 44→45, 46→47, 48→50 | Total négatif, zone invalide, gratuité et tarif intérieur |

La colonne `Cover` initiale affiche 58 %, mais ce n'est pas le taux de
branches seul. Elle combine lignes et branches :
`(23 + 8) / (35 + 18) = 58,49 %`. Le taux de branches vient des champs
`covered_branches` et `num_branches` du JSON.

La suite finale couvre toutes les branches mesurées, y compris lors des tests
en échec. Cela ne démontre pas l'absence de défauts : le plafond et le contrôle
du caractère entier sont absents du code, donc absents du dénominateur de
couverture. coverage.py mesure les arcs entre lignes, pas séparément chaque
sous-condition d'un `and` ou d'un `or` (chapitre 9, pages 6, 17 et 50).
Ce rapport ne revendique pas une mesure MC/DC.

Commandes reproductibles, après activation de l'environnement Python :

```powershell
python -m pytest tests/test_panier.py::test_total_un_article tests/test_panier.py::test_frais_grand_tunis --cov=panier --cov-branch --cov-report=term-missing --cov-report=json:resultats/couverture_initiale.json
python -m pytest --cov=panier --cov-branch --cov-report=term-missing --cov-report=json:resultats/couverture_finale.json
python verifier_mutants.py
```

Sur la machine utilisée, `python` n'était pas dans le PATH. L'exécutable était
`.\myvenv\Scripts\python.exe`. Le code de sortie **1** de la suite finale
est normal ici : il signale les sept échecs que le sujet demande de conserver.

### Sortie réelle de la suite finale

<!--SORTIE_FINALE-->

## Tâche 4 - Mutants

La commande `python verifier_mutants.py` a été exécutée avec la suite finale.
Le script compare chaque mutant à `panier.py`. Les sept tests déjà en échec
sur l'original sont exclus des tests pouvant tuer un mutant. Les témoins
ci-dessous font donc partie des 77 tests réussis sur l'original.

| Mutant | Résultat | Test qui le tue | Différence observée ou justification |
|---|---|---|---|
| mutant_1 | Tué | `test_total_deux_lignes` | 13,600 DT attendus ; l'addition remplaçant la multiplication donne 10,700 DT |
| mutant_2 | Tué | `test_total_prix_non_positif[nul]` | Le prix 0 doit lever `ValueError`, mais le mutant l'accepte |
| mutant_3 | Tué | `test_remise_code_different_ignore[casse_mixte]` | Adhérent à 200 DT : 40 DT attendus, mais le mutant calcule 20 % de 150, soit 30 DT |
| mutant_4 | Tué | `test_remise_code_different_ignore[casse_mixte]` | Même cas : 40 DT attendus, mais le mutant réserve la remise aux non-adhérents et renvoie 0 |
| mutant_5 | Tué | `test_remise_code_au_plafond_et_apres[egal_3]` | 3 DT attendus ; le mutant soustrait le bonus et renvoie -3 DT |
| mutant_6 | Tué | `test_frais_payants_sous_seuil[total_nul-GRAND_TUNIS-6.0]` | Total 0 autorisé, frais attendus 6 DT ; le mutant lève `ValueError` |
| mutant_7 | Tué | `test_frais_grand_tunis` | Zone valide, frais attendus 6 DT ; la condition inversée lève `ValueError` |
| mutant_8 | Survivant équivalent | Aucun | Le contrôle explicite de `None` est redondant, démonstration ci-dessous |

Pour le mutant 8, on compare les conditions suivantes :

```python
# Original
code_promo is not None and code_promo == "LISTE3"
# Mutant
code_promo == "LISTE3"
```

- Si le code est `None`, la première condition est fausse. La seconde l'est
  aussi puisque `None != "LISTE3"`.
- S'il n'est pas `None`, la première partie de la condition originale est
  vraie : les deux versions évaluent la même égalité.

Pour les entrées prévues (code texte ou `None`), les deux versions ajoutent
donc toujours le même montant. Le reste du programme est identique. Aucun
test du domaine spécifié ne peut tuer ce mutant ; sa survie n'est pas seulement
justifiée par l'absence d'échec dans la suite.

Le script affiche **7/8** (87,5 % brut). En excluant le mutant équivalent,
le score demandé est **7 / (8 - 1) = 7/7 = 100 %**.
Ce score concerne les huit mutants fournis, pas toutes les fautes possibles.
La sortie complète est dans [resultats/mutants.txt](resultats/mutants.txt).

## Tâche 5 - Défauts

Les trois défauts restent ouverts. La sévérité traduit l'effet sur le résultat ;
la priorité proposée traduit l'ordre de correction. Le module n'a pas été corrigé.

### DEF-01 - Livraison payante au seuil inclus

| Champ | Contenu |
|---|---|
| Titre | Des frais sont facturés pour un total de 70 DT |
| Fonction | `frais_livraison` |
| Étapes pour reproduire | Importer la fonction, puis appeler `frais_livraison(70.0, "GRAND_TUNIS", False)` |
| Résultat attendu | 0,000 DT : `SPECIFICATION.md`, §3, gratuité dès 70 DT, seuil inclus |
| Résultat obtenu | 6,000 DT ; avec `"INTERIEUR"`, 9,000 DT au lieu de 0 |
| Effet | Le client paie une livraison annoncée gratuite |
| Sévérité | Majeure : montant facturé incorrect |
| Priorité | Haute : seuil commercial directement visible |
| Technique qui l'a révélé | Analyse à 2 valeurs : 69,999 et 70,000 DT |
| Test qui le révèle | `test_frais_gratuits_au_seuil`, dans les deux zones |
| Cause repérée à la relecture | Ligne 46 : comparaison stricte `>` au lieu d'inclure le seuil |

### DEF-02 - Remise supérieure au total

| Champ | Contenu |
|---|---|
| Titre | Le bonus de 3 DT n'est pas plafonné au montant du panier |
| Fonction | `remise` |
| Étapes pour reproduire | Importer la fonction, puis appeler `remise(2.0, False, "LISTE3")` |
| Résultat attendu | 2,000 DT : `SPECIFICATION.md`, §2, la remise ne dépasse jamais le total |
| Résultat obtenu | 3,000 DT |
| Effet | Le calcul `total - remise` produirait -1 DT à payer |
| Sévérité | Majeure : montant monétaire incohérent |
| Priorité | Haute : touche les petits paniers utilisant le code promo |
| Technique qui l'a révélé | Test de la règle du plafond, complété à 0 et 2,999 DT |
| Test qui le révèle | `test_remise_plafonnee_au_total`, quatre paramètres |
| Cause repérée à la relecture | Ligne 37 : retour du montant arrondi sans appliquer de plafond |

### DEF-03 - Quantité fractionnaire acceptée

| Champ | Contenu |
|---|---|
| Titre | Une quantité de 1,5 est acceptée |
| Fonction | `total_panier` |
| Étapes pour reproduire | Importer la fonction, puis appeler `total_panier([(2.0, 1.5)])` |
| Résultat attendu | `ValueError` : `SPECIFICATION.md`, §1, quantité entière de 1 à 20, sinon exception |
| Résultat obtenu | 3,000 DT, sans exception |
| Effet | Une entrée interdite par la règle métier est utilisée dans le calcul |
| Sévérité | Majeure : validation obligatoire manquante |
| Priorité | Moyenne : à corriger après les deux erreurs de facturation |
| Technique qui l'a révélé | Partition invalide « quantité non entière » ; voir aussi chapitre 8, page 11 |
| Test qui le révèle | `test_total_quantite_non_entiere` |
| Cause repérée à la relecture | Ligne 24 : seules les bornes sont contrôlées, pas le caractère entier |

Les sept échecs se répartissent en 2 pour DEF-01, 4 pour DEF-02 et 1 pour DEF-03.
Les autres cas réussissent.

## Tâche 5 - Journal d'usage de l'IA

Outil : **ChatGPT / Codex**. Les entrées détaillent les étapes d'une même
demande d'aide, le 15 novembre 2026. L'aide a porté sur la conception et
l'écriture des tests, l'exécution des outils, l'analyse des résultats et la
rédaction du rapport. Les chiffres proviennent des commandes exécutées et
des fichiers conservés dans `resultats/`.

| N° | Outil | Demande ou étape | Production de l'IA | Vérification, conservation ou correction |
|---|---|---|---|---|
| 1 | Codex | Lire le README, la spécification et les chapitres | Repérage des livrables, partitions, limites au millime et table à six règles | Les seuils du groupe sont conservés ; les chiffres des exemples du cours ne sont pas recopiés |
| 2 | Codex | Écrire les tests demandés en français | Suite pytest paramétrée, dont le seuil, le plafond et la quantité non entière | Les attendus correspondent aux règles de la spécification ; les sept échecs sont conservés selon le README |
| 3 | Codex | Exécuter Python pour préparer les mesures | Première commande utilisant `python` sans vérifier sa présence dans le PATH | Erreur réelle : PowerShell a répondu que `python` n'était pas reconnu. La commande a été remplacée par le chemin de l'interpréteur de `myvenv` ; l'accès a aussi nécessité une autorisation hors du bac à sable |
| 4 | Codex | Mesurer la couverture et analyser les mutants | Sorties des commandes, calcul 8/18 puis 18/18, analyse du mutant 8 | Le JSON sert au calcul des branches ; le score brut 7/8 reste distingué du score 7/7 hors équivalent |
| 5 | Codex | Préparer le rapport et l'archive | Tableaux, trois fiches de défaut, traces et explications du cours | Les noms et la date de remise restent à renseigner ; aucune validation personnelle des étudiants n'est prétendue |

**Erreur de l'IA effectivement repérée et corrigée pendant la session :**
l'hypothèse que la commande `python` était disponible dans le terminal était
fausse. Le message `CommandNotFoundException` l'a montré. L'utilisation de
`.\myvenv\Scripts\python.exe` a ensuite permis l'exécution des deux tests
initiaux et de la suite complète. Il s'agit d'une erreur de préparation
de l'environnement, pas d'un résultat attendu volontairement inventé.
La correction a été effectuée pendant l'assistance ; les membres doivent
encore relire et s'approprier le travail avant de le présenter.

## Parties du cours utilisées

Les pages correspondent aux numéros de page des PDF fournis.

| Support | Pages | Application au projet |
|---|---|---|
| Chapitre 8, *Conception des Tests : Techniques Boîte Noire et Basées sur l'Expérience* | 5-6, 8-12 | Attendus issus de la spécification ; partitions valides et invalides, une entrée invalide à la fois |
| Même chapitre | 21-26 | Analyse à deux valeurs : 0/1, 20/21, -0,001/0 et 69,999/70 |
| Même chapitre | 28-30, 52 | Table complète, fusion des colonnes et ajout des tests aux seuils |
| Même chapitre | 53 | Vérification des propositions de l'IA et de leurs attendus |
| Chapitre 9, *Test Boîte Blanche : Couverture du Code et Test de Mutation* | 5-6, 17, 19-20 | Complément entre boîte noire et boîte blanche ; limites de la couverture |
| Même chapitre | 42 | Boucle testée avec 0, 1 et 2 lignes |
| Même chapitre | 49-52 | Mesure avec pytest-cov et lecture des arcs entre lignes |
| Même chapitre | 54-58 | Tests tueurs, survivants, équivalence et score de mutation |
| Même chapitre | 63 | Oracle tiré de la spécification, jamais recopié du comportement bogué |

Le chapitre 7 n'a pas été fourni. Les fiches de défaut suivent donc les champs
du modèle `RAPPORT.md`, sans attribuer au chapitre 7 un contenu qui n'a pas été lu.

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
