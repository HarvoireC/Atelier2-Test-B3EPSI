import unittest
import os
import shutil
import tempfile
from Atelier2 import FileManager

class TestFileManagerFilesOnly(unittest.TestCase):
    def setUp(self):
        # Créer un répertoire temporaire pour les tests
        self.test_dir = tempfile.mkdtemp()
        self.fm = FileManager()
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

    # --- Tests delete_files ---
    
    def test_delete_files_usual_single(self):
        # Cas usuel : un seul fichier
        self.fm.file_selector.selected_files = [self.file1]
        self.fm.delete_files()
        self.assertFalse(os.path.exists(self.file1))
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    def test_delete_files_multiple(self):
        # Cas usuel : plusieurs fichiers
        self.fm.file_selector.selected_files = [self.file1, self.file2]
        self.fm.delete_files()
        self.assertFalse(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))

    def test_delete_files_none_selected(self):
        # Cas extrême : aucun fichier sélectionné
        self.fm.file_selector.selected_files = []
        self.fm.delete_files() # Ne doit pas planter
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    def test_delete_files_non_existent(self):
        # Cas d'erreur : fichier dans la liste n'existe pas physiquement
        ghost = os.path.join(self.test_dir, "ghost.txt")
        self.fm.file_selector.selected_files = [ghost]
        self.fm.delete_files() # Doit ignorer ou gérer l'erreur gracieusement
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    # --- Tests copy_files ---

    def test_copy_files_usual(self):
        # Cas usuel : copier un fichier vers un dossier existant
        dest_dir = os.path.join(self.test_dir, "dest")
        os.mkdir(dest_dir)
        self.fm.file_selector.selected_files = [self.file1]
        self.fm.copy_files(dest_dir)
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "file1.txt")))
        self.assertTrue(os.path.exists(self.file1)) # L'original reste

    def test_copy_files_to_new_path(self):
        # Cas : copier vers un nouveau chemin de fichier
        dest_file = os.path.join(self.test_dir, "file1_copy.txt")
        self.fm.file_selector.selected_files = [self.file1]
        self.fm.copy_files(dest_file)
        self.assertTrue(os.path.exists(dest_file))

    def test_copy_files_non_existent_source(self):
        # Cas d'erreur : source n'existe pas
        ghost = os.path.join(self.test_dir, "ghost.txt")
        self.fm.file_selector.selected_files = [ghost]
        self.fm.copy_files(self.test_dir)
        # Ne devrait pas lever d'exception non gérée

    def test_copy_files_no_selection(self):
        self.fm.file_selector.selected_files = []
        self.fm.copy_files(self.test_dir)
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

    # --- Tests move_files ---

    def test_move_files_usual(self):
        # Cas usuel : déplacer un fichier vers un dossier existant
        dest_dir = os.path.join(self.test_dir, "dest_move")
        os.mkdir(dest_dir)
        self.fm.file_selector.selected_files = [self.file1]
        self.fm.move_files(dest_dir)
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "file1.txt")))
        self.assertFalse(os.path.exists(self.file1)) # L'original est parti

    def test_move_files_to_non_existent_dir(self):
        # Cas extrême : destination n'existe pas (devrait être créée par le move ou gérée)
        dest_dir = os.path.join(self.test_dir, "auto_create_dir")
        self.fm.file_selector.selected_files = [self.file2]
        self.fm.move_files(dest_dir)
        # Actuellement shutil.move gère la création si c'est un chemin de fichier, 
        # mais si on veut un dossier on verra comment c'est géré.
        self.assertTrue(os.path.exists(dest_dir))
        self.assertFalse(os.path.exists(self.file2))

    def test_move_files_no_selection(self):
        self.fm.file_selector.selected_files = []
        self.fm.move_files(self.test_dir)
        self.assertEqual(len(self.fm.file_selector.selected_files), 0)

if __name__ == "__main__":
    unittest.main()
