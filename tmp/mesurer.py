"""Conserve les sorties réelles des commandes du README en UTF-8."""
import os
from pathlib import Path
import subprocess
import sys

racine = Path(__file__).resolve().parents[1]
sorties = racine / "resultats"
sorties.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONIOENCODING="utf-8")
commandes = [
    ("tests_initiaux.txt", ["-m", "pytest", "tests/test_panier.py::test_total_un_article",
        "tests/test_panier.py::test_frais_grand_tunis", "--cov=panier", "--cov-branch",
        "--cov-report=term-missing", "--cov-report=json:resultats/couverture_initiale.json"]),
    ("tests_finaux.txt", ["-m", "pytest", "--cov=panier", "--cov-branch",
        "--cov-report=term-missing", "--cov-report=json:resultats/couverture_finale.json"]),
    ("mutants.txt", ["verifier_mutants.py"]),
]
for nom, arguments in commandes:
    execution = subprocess.run([sys.executable, *arguments], cwd=racine, env=env,
                               capture_output=True, text=True, encoding="utf-8")
    (sorties / nom).write_text(execution.stdout + execution.stderr, encoding="utf-8")
    print(nom, "code de sortie :", execution.returncode, flush=True)
    print(execution.stdout[-2500:], flush=True)
