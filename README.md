# Atelier 2 - Test : Gestionnaire de Fichiers (FileManager)

Ce projet est réalisé dans le cadre de l'Atelier 2 portant sur les tests unitaires et l'approche TDD (Test Driven Development) en Python. L'objectif est de sécuriser une application de gestion de fichiers en simulant ses dépendances et en gérant les cas d'erreurs via une interface utilisateur.

## Structure du Projet

- `Atelier2.py` : Contient la logique métier (`FileManager`), la gestion de la sélection (`FileSelector`) et l'interface utilisateur (`UserInterface`).
- `test_atelier2.py` : Suite de tests unitaires utilisant `unittest` et `unittest.mock`.

## Fonctionnalités de FileManager

La classe `FileManager` permet d'effectuer les opérations suivantes sur une sélection de fichiers :
- **Copie** (`copy_files`) : Copie les fichiers sélectionnés vers une destination.
- **Déplacement** (`move_files`) : Déplace les fichiers sélectionnés vers une destination.
- **Suppression** (`delete_files`) : Supprime les fichiers sélectionnés.

## Étapes de réalisation

### Étape 1 : Mise en place et configuration
- Initialisation du projet à partir de la correction proposée.
- Vérification de l'installation et de la configuration par le lancement des tests initiaux.

### Étape 2 : Tests unitaires et Robustesse
- Écriture des tests unitaires pour les méthodes `delete_files`, `copy_files` et `move_files`.
- Prise en compte des cas :
  - **Usuels** : Opérations nominales sur des fichiers existants.
  - **Extrêmes** : Aucune sélection, dossiers inexistants.
  - **Erreurs** : Fichiers verrouillés, erreurs d'E/S (E/S).
- Correction de la classe `FileManager` pour garantir le passage de tous les tests.

### Étape 3 : Évolutions et Approche TDD
Ajout d'une gestion interactive des erreurs via la propriété `error_choice` de `UserInterface`. En cas d'erreur lors d'une opération, l'utilisateur peut choisir entre :
- **0 : Ignorer** l'erreur actuelle et continuer le traitement du fichier suivant.
- **1 : Toujours ignorer** toutes les erreurs suivantes pour l'opération en cours.
- **2 : Stopper** l'opération immédiatement.

Cette étape a été réalisée suivant le cycle TDD :
1. Ajout d'un cas de test pour un choix spécifique.
2. Vérification de l'échec du test.
3. Implémentation du code minimal pour faire passer le test.
4. Refactorisation.

## Lancement des tests

Pour exécuter la suite de tests unitaires, utilisez la commande suivante :

```bash
python -m unittest test_atelier2.py
```

## Dépendances
- Python 3.x
- Modules standards : `os`, `shutil`, `unittest`, `unittest.mock`
