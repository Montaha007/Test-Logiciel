# Les 8 mutants — groupe 05

Chaque fichier `mutant_N.py` est une copie de `panier.py` avec une seule modification.

| Mutant | Fonction | Ligne | Code original | Code du mutant |
|---|---|---|---|---|
| mutant_1 | `total_panier` | 26 | `total += prix * quantite` | `total += prix + quantite` |
| mutant_2 | `total_panier` | 22 | `if prix <= 0:` | `if prix < 0:` |
| mutant_3 | `remise` | 34 | `montant += total * TAUX_REMISE / 100` | `montant += SEUIL_REMISE * TAUX_REMISE / 100` |
| mutant_4 | `remise` | 33 | `if adherent and total >= SEUIL_REMISE:` | `if not adherent and total >= SEUIL_REMISE:` |
| mutant_5 | `remise` | 36 | `montant += REMISE_CODE` | `montant -= REMISE_CODE` |
| mutant_6 | `frais_livraison` | 42 | `if total < 0:` | `if total <= 0:` |
| mutant_7 | `frais_livraison` | 44 | `if zone not in ZONES:` | `if zone in ZONES:` |
| mutant_8 | `remise` | 35 | `if code_promo is not None and code_promo == CODE_PROMO:` | `if code_promo == CODE_PROMO:` |

Commande : `python verifier_mutants.py`. Un mutant est tué si au moins un test qui réussit sur `panier.py` échoue sur le mutant.
