import unittest
import os
import shutil
import tempfile
from unittest.mock import MagicMock, patch
from Atelier2 import FileManager, UserInterface

class TestFileManagerFilesOnly(unittest.TestCase):
    def setUp(self):
        # Créer un répertoire temporaire pour les tests
        self.test_dir = tempfile.mkdtemp()
        self.ui = UserInterface()
        self.fm = FileManager(ui=self.ui)
        self.fm.current_path = self.test_dir
        
        # Créer des fichiers de test
        self.file1 = os.path.join(self.test_dir, "file1.txt")
        with open(self.file1, "w") as f:
            f.write("test content 1")
            
        self.file2 = os.path.join(self.test_dir, "file2.txt")
        with open(self.file2, "w") as f:
            f.write("test content 2")

    def tearDown(self):
        # Nettoyer
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        # Afficher le résultat du test
        print(f"\n{self._testMethodName} : OK")

    # --- Tests delete_files ---
    
    def test_delete_files_usual_single(self):
        # Cas usuel : un seul fichier
        self.fm.file_selector.selected_files = [self.file1]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.delete_files()
        self.assertFalse(os.path.exists(self.file1))
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    def test_delete_files_multiple(self):
        # Cas usuel : plusieurs fichiers
        self.fm.file_selector.selected_files = [self.file1, self.file2]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.delete_files()
        self.assertFalse(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))

    def test_delete_files_none_selected(self):
        # Cas extrême : aucun fichier sélectionné
        self.fm.file_selector.selected_files = []
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.delete_files() # Ne doit pas planter
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    def test_delete_files_non_existent(self):
        # Cas d'erreur : fichier dans la liste n'existe pas physiquement
        ghost = os.path.join(self.test_dir, "ghost.txt")
        self.fm.file_selector.selected_files = [ghost]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.delete_files() # Doit ignorer ou gérer l'erreur gracieusement
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    # --- Tests copy_files ---

    def test_copy_files_usual(self):
        # Cas usuel : copier un fichier vers un dossier existant
        dest_dir = os.path.join(self.test_dir, "dest")
        os.mkdir(dest_dir)
        self.fm.file_selector.selected_files = [self.file1]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.copy_files(dest_dir)
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "file1.txt")))
        self.assertTrue(os.path.exists(self.file1)) # L'original reste

    def test_copy_files_to_new_path(self):
        # Cas : copier vers un nouveau chemin de fichier
        dest_file = os.path.join(self.test_dir, "file1_copy.txt")
        self.fm.file_selector.selected_files = [self.file1]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.copy_files(dest_file)
        self.assertTrue(os.path.exists(dest_file))

    def test_copy_files_non_existent_source(self):
        # Cas d'erreur : source n'existe pas
        ghost = os.path.join(self.test_dir, "ghost.txt")
        self.fm.file_selector.selected_files = [ghost]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.copy_files(self.test_dir)
        # Ne devrait pas lever d'exception non gérée

    def test_copy_files_no_selection(self):
        self.fm.file_selector.selected_files = []
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.copy_files(self.test_dir)
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    # --- Tests move_files ---

    def test_move_files_usual(self):
        # Cas usuel : déplacer un fichier vers un dossier existant
        dest_dir = os.path.join(self.test_dir, "dest_move")
        os.mkdir(dest_dir)
        self.fm.file_selector.selected_files = [self.file1]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.move_files(dest_dir)
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "file1.txt")))
        self.assertFalse(os.path.exists(self.file1)) # L'original est parti

    def test_move_files_to_non_existent_dir(self):
        # Cas extrême : destination n'existe pas (devrait être créée par le move ou gérée)
        dest_dir = os.path.join(self.test_dir, "auto_create_dir")
        self.fm.file_selector.selected_files = [self.file2]
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.move_files(dest_dir)
        # Actuellement shutil.move gère la création si c'est un chemin de fichier.
        self.assertTrue(os.path.exists(dest_dir))
        self.assertFalse(os.path.exists(self.file2))

    def test_move_files_no_selection(self):
        self.fm.file_selector.selected_files = []
        with patch('sys.stdout', new=unittest.mock.MagicMock()):
            self.fm.move_files(self.test_dir)
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    # --- Tests Error Handling TDD ---

    def test_delete_files_error_choice_0_ignore(self):
        """TDD: Choix 0 - Ignorer l'erreur et continuer"""
        # Créer un fichier qui sera difficile à supprimer (simulé par mock)
        self.fm.file_selector.selected_files = [self.file1, self.file2]
        
        # Simuler un retour de ui.error_choice = 0
        with patch('Atelier2.UserInterface.error_choice', new_callable=unittest.mock.PropertyMock) as mock_choice:
            mock_choice.return_value = 0
            
            # Faire en sorte que os.remove lève une erreur pour le premier fichier uniquement
            original_remove = os.remove
            def side_effect(path):
                if path == self.file1:
                    raise OSError("Fichier verrouillé")
                return original_remove(path)
            
            with patch('os.remove', side_effect=side_effect):
                self.fm.delete_files()
                
        # Vérifier que file2 a été supprimé malgré l'erreur sur file1
        self.assertFalse(os.path.exists(self.file2))
        self.assertTrue(os.path.exists(self.file1)) # file1 n'a pas pu être supprimé
        # Le sélecteur doit être vidé si on a continué jusqu'au bout
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    def test_delete_files_error_choice_1_always_ignore(self):
        """TDD: Choix 1 - Toujours ignorer les erreurs"""
        # Créer 3 fichiers
        file3 = os.path.join(self.test_dir, "file3.txt")
        with open(file3, "w") as f: f.write("test3")
        
        self.fm.file_selector.selected_files = [self.file1, self.file2, file3]
        
        # Simuler un retour de ui.error_choice = 1 au premier appel
        # On utilise une liste d'effets de bord pour vérifier combien de fois c'est appelé
        with patch('Atelier2.UserInterface.error_choice', new_callable=unittest.mock.PropertyMock) as mock_choice:
            mock_choice.return_value = 1
            
            # Faire en sorte que os.remove lève une erreur pour TOUS les fichiers
            with patch('os.remove', side_effect=OSError("Verrouillé")):
                self.fm.delete_files()
            
            # error_choice ne doit être appelé qu'une seule fois grâce au flag always_ignore
            self.assertEqual(mock_choice.call_count, 1)
                
        # Les fichiers existent toujours car l'erreur a été ignorée (mais l'opération n'a pas réussi à les supprimer)
        self.assertTrue(os.path.exists(self.file1))
        self.assertTrue(os.path.exists(self.file2))
        self.assertTrue(os.path.exists(file3))
        # Le sélecteur doit être vidé car on a parcouru toute la liste
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    def test_delete_files_error_choice_2_stop(self):
        """TDD: Choix 2 - Stopper l'opération"""
        self.fm.file_selector.selected_files = [self.file1, self.file2]
        
        with patch('Atelier2.UserInterface.error_choice', new_callable=unittest.mock.PropertyMock) as mock_choice:
            mock_choice.return_value = 2
            
            with patch('os.remove', side_effect=OSError("Verrouillé")):
                self.fm.delete_files()
            
            # error_choice doit être appelé une fois
            self.assertEqual(mock_choice.call_count, 1)
                
        # file1 et file2 existent toujours
        self.assertTrue(os.path.exists(self.file1))
        self.assertTrue(os.path.exists(self.file2))
        # Le sélecteur ne doit PAS être vidé car l'opération a été stoppée prématurément
        # (c'est un choix de design, on peut discuter, mais "Stopper" suggère d'arrêter tout de suite)
        self.assertEqual(len(self.fm.file_selector.selected_files), 2)

    def test_copy_files_error_choice_0_ignore(self):
        """TDD: copy_files - Choix 0 - Ignorer"""
        self.fm.file_selector.selected_files = [self.file1, self.file2]
        dest = os.path.join(self.test_dir, "dest")
        
        with patch('Atelier2.UserInterface.error_choice', new_callable=unittest.mock.PropertyMock) as mock_choice:
            mock_choice.return_value = 0
            
            with patch('shutil.copy2', side_effect=[OSError("Failed"), None]):
                self.fm.copy_files(dest)
        
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    def test_move_files_error_choice_2_stop(self):
        """TDD: move_files - Choix 2 - Stopper"""
        self.fm.file_selector.selected_files = [self.file1, self.file2]
        dest = os.path.join(self.test_dir, "dest")
        
        with patch('Atelier2.UserInterface.error_choice', new_callable=unittest.mock.PropertyMock) as mock_choice:
            mock_choice.return_value = 2
            
            with patch('shutil.move', side_effect=OSError("Failed")):
                self.fm.move_files(dest)
        
        # Le sélecteur doit encore contenir les 2 fichiers
        self.assertEqual(len(self.fm.file_selector.selected_files), 2)

if __name__ == "__main__":
    unittest.main()
