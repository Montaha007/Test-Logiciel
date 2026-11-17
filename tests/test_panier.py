"""Tests issus de SPECIFICATION.md, groupe 05.

Les échecs qui révèlent les défauts du module sont volontairement conservés.
Les valeurs attendues sont calculées à partir des règles, sans importer les
constantes de panier.py. Les deux tests de départ sont conservés.
"""
import pytest

from panier import total_panier, remise, frais_livraison


def test_total_un_article():
    assert total_panier([(2.0, 3)]) == pytest.approx(6.0)


def test_frais_grand_tunis():
    assert frais_livraison(10.0, "GRAND_TUNIS") == pytest.approx(6.000)


# Tâche 1 : total, partitions invalides, limites et boucle.
def test_total_panier_vide():
    assert total_panier([]) == 0.000


def test_total_deux_lignes():
    # 2,5 × 4 + 1,2 × 3 = 13,6 DT.
    assert total_panier([(2.5, 4), (1.2, 3)]) == pytest.approx(
        13.600, rel=0, abs=1e-9
    )


@pytest.mark.parametrize("quantite, attendu", [(1, 2.0), (20, 40.0)],
                         ids=["minimum_1", "maximum_20"])
def test_total_quantite_aux_bornes_valides(quantite, attendu):
    assert total_panier([(2.0, quantite)]) == pytest.approx(attendu, rel=0, abs=1e-9)


@pytest.mark.parametrize("quantite", [0, 21], ids=["sous_minimum_0", "sur_maximum_21"])
def test_total_quantite_hors_bornes(quantite):
    with pytest.raises(ValueError):
        total_panier([(2.0, quantite)])


def test_total_quantite_non_entiere():
    with pytest.raises(ValueError):
        total_panier([(2.0, 1.5)])


@pytest.mark.parametrize("prix", [-0.001, 0.0], ids=["negatif", "nul"])
def test_total_prix_non_positif(prix):
    with pytest.raises(ValueError):
        total_panier([(prix, 1)])


def test_total_prix_un_millime():
    assert total_panier([(0.001, 1)]) == pytest.approx(0.001, rel=0, abs=1e-9)


@pytest.mark.parametrize("ligne", [(0.0, 1), (2.0, 21)],
                         ids=["prix_invalide", "quantite_invalide"])
def test_total_verifie_aussi_la_deuxieme_ligne(ligne):
    with pytest.raises(ValueError):
        total_panier([(2.0, 3), ligne])


@pytest.mark.parametrize("prix, attendu", [(1.2344, 1.234), (1.2346, 1.235)],
                         ids=["arrondi_inferieur", "arrondi_superieur"])
def test_total_arrondi_au_millime(prix, attendu):
    assert total_panier([(prix, 1)]) == pytest.approx(attendu, rel=0, abs=1e-9)


# Tâche 1 : livraison. Une seule entrée invalide par cas.
@pytest.mark.parametrize("zone, tarif", [("GRAND_TUNIS", 6.0), ("INTERIEUR", 9.0)])
@pytest.mark.parametrize("total", [0.0, 25.0, 69.999],
                         ids=["total_nul", "payant_courant", "juste_sous_seuil"])
def test_frais_payants_sous_seuil(total, zone, tarif):
    assert frais_livraison(total, zone) == pytest.approx(tarif, rel=0, abs=1e-9)


@pytest.mark.parametrize("zone", ["GRAND_TUNIS", "INTERIEUR"])
def test_frais_gratuits_au_seuil(zone):
    assert frais_livraison(70.0, zone) == 0.000


@pytest.mark.parametrize("zone", ["GRAND_TUNIS", "INTERIEUR"])
@pytest.mark.parametrize("total", [70.001, 100.0], ids=["juste_au_dessus", "au_dessus"])
def test_frais_gratuits_au_dessus_du_seuil(total, zone):
    assert frais_livraison(total, zone) == 0.000


@pytest.mark.parametrize("zone", ["GRAND_TUNIS", "INTERIEUR"])
@pytest.mark.parametrize("total", [0.0, 10.0, 70.0, 100.0])
def test_frais_premium_gratuits(total, zone):
    assert frais_livraison(total, zone, premium=True) == 0.000


@pytest.mark.parametrize("zone", ["GRAND_TUNIS", "INTERIEUR"])
@pytest.mark.parametrize("premium", [False, True], ids=["standard", "premium"])
def test_frais_total_negatif_refuse(zone, premium):
    with pytest.raises(ValueError):
        frais_livraison(-0.001, zone, premium)


@pytest.mark.parametrize("zone", ["SFAX", "grand_tunis", "", None],
                         ids=["inconnue", "mauvaise_casse", "vide", "absente"])
@pytest.mark.parametrize("premium", [False, True], ids=["standard", "premium"])
@pytest.mark.parametrize("total", [10.0, 100.0], ids=["sous_seuil", "au_dessus"])
def test_frais_zone_invalide_meme_si_gratuite(total, premium, zone):
    with pytest.raises(ValueError):
        frais_livraison(total, zone, premium)


# Tâche 2 : un cas par colonne de la table simplifiée, puis compléments.
@pytest.mark.parametrize(
    "total, adherent, code, attendu",
    [
        (200.0, True, "LISTE3", 43.0),
        (200.0, True, None, 40.0),
        (100.0, True, "LISTE3", 3.0),
        (100.0, True, None, 0.0),
        (200.0, False, "LISTE3", 3.0),
        (200.0, False, None, 0.0),
    ],
    ids=["S1_cumul", "S2_adherent_seul", "S3_promo_sous_seuil",
         "S4_aucune_sous_seuil", "S5_promo_non_adherent", "S6_aucune_non_adherent"],
)
def test_remise_table_simplifiee(total, adherent, code, attendu):
    assert remise(total, adherent, code) == pytest.approx(attendu, rel=0, abs=1e-9)


@pytest.mark.parametrize("code, attendu", [("LISTE3", 3.0), (None, 0.0)],
                         ids=["R7_promo", "R8_sans_promo"])
def test_remise_non_adherent_sous_seuil(code, attendu):
    assert remise(100.0, False, code) == pytest.approx(attendu, rel=0, abs=1e-9)


@pytest.mark.parametrize("total, code, attendu", [
    (149.999, None, 0.0), (150.0, None, 30.0),
    (149.999, "LISTE3", 3.0), (150.0, "LISTE3", 33.0),
], ids=["sous_seuil", "seuil_inclus", "sous_seuil_promo", "seuil_cumul"])
def test_remise_limites_seuil_adherent(total, code, attendu):
    assert remise(total, True, code) == pytest.approx(attendu, rel=0, abs=1e-9)


@pytest.mark.parametrize("code", ["liste3", "Liste3", "LISTE3 ", " LISTE3", "", "AUTRE"],
                         ids=["minuscules", "casse_mixte", "espace_fin", "espace_debut",
                              "vide", "inconnu"])
def test_remise_code_different_ignore(code):
    # Le code invalide n'annule pas la remise adhérent de 40 DT.
    assert remise(200.0, True, code) == pytest.approx(40.0, rel=0, abs=1e-9)


@pytest.mark.parametrize("adherent", [False, True], ids=["non_adherent", "adherent"])
def test_remise_total_nul_sans_code(adherent):
    assert remise(0.0, adherent) == 0.000


@pytest.mark.parametrize("total, adherent", [(0.0, False), (2.0, False),
                                           (2.0, True), (2.999, False)],
                         ids=["nul", "petit_total", "petit_total_adherent", "juste_sous_3"])
def test_remise_plafonnee_au_total(total, adherent):
    assert remise(total, adherent, "LISTE3") == pytest.approx(total, rel=0, abs=1e-9)


@pytest.mark.parametrize("total", [3.0, 3.001], ids=["egal_3", "juste_apres_3"])
def test_remise_code_au_plafond_et_apres(total):
    assert remise(total, False, "LISTE3") == pytest.approx(3.0, rel=0, abs=1e-9)


@pytest.mark.parametrize("total, attendu", [(150.002, 30.000), (150.003, 30.001)],
                         ids=["arrondi_inferieur", "arrondi_superieur"])
def test_remise_arrondie_au_millime(total, attendu):
    assert remise(total, True) == pytest.approx(attendu, rel=0, abs=1e-9)
