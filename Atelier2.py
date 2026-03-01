import os
import shutil

""" File Manager Console Application
    Generated with Claude 3.5 Haiku
    With 2 prompts :
        Génère un programme console python qui permet d'explorer les fichiers,
        en sélectionner pour copier, déplacer et supprimer les fichiers sélectionnés.
        Une classe "métier" regroupe les fonctions de sélection, copie, déplacement
        et suppression.

        Deux rectifications : il faudrait passer le code et l'interface en anglais
        et sortir la sélection de la classe "métier" 
"""


class UserInterface:
    def __init__(self):
        self._error_choice = 0

    @property
    def error_choice(self):
        return self._error_choice

    @error_choice.setter
    def error_choice(self, value):
        self._error_choice = value


class FileSelector:
    def __init__(self):
        self.selected_files = []
        self.current_directory_contents = []

    def load_directory_contents(self, directory_path):
        """Load the contents of a directory"""
        try:
            self.current_directory_contents = os.listdir(directory_path)
            return self.current_directory_contents
        except Exception as e:
            print(f"Error loading directory contents: {e}")
            return []

    def select_files_by_indices(self, indices, directory_path):
        """Select files based on indices"""
        try:
            # Convert input string to list of indices
            selected_indices = [int(i.strip()) for i in indices.split(',')]

            # Reset previous selection
            self.selected_files.clear()

            # Select files
            for index in selected_indices:
                if 0 <= index < len(self.current_directory_contents):
                    full_path = os.path.join(directory_path, self.current_directory_contents[index])
                    self.selected_files.append(full_path)

            print("Selected files:")
            for file in self.selected_files:
                print(f" - {os.path.basename(file)}")

            return self.selected_files
        except ValueError:
            print("Invalid input. Please enter valid indices.")
            return []
        except Exception as e:
            print(f"Error selecting files: {e}")
            return []

    def get_selected_files(self):
        """Return the list of currently selected files"""
        return self.selected_files

    def clear_selection(self):
        """Clear the current file selection"""
        self.selected_files.clear()


class FileManager:
    def __init__(self, ui=None):
        self.current_path = os.path.expanduser('~')
        self.file_selector = FileSelector()
        self.ui = ui if ui else UserInterface()

    def display_directory_contents(self):
        """Display contents of the current directory"""
        try:
            contents = self.file_selector.load_directory_contents(self.current_path)
            print(f"\nCurrent Directory: {self.current_path}")
            print("-" * 50)
            for index, element in enumerate(contents):
                full_path = os.path.join(self.current_path, element)
                element_type = "📁 Folder" if os.path.isdir(full_path) else "📄 File"
                print(f"{index}. {element_type}: {element}")
        except PermissionError:
            print("Access denied to this directory.")
        except Exception as e:
            print(f"Error: {e}")

    def navigate(self, index):
        """Navigate to a subdirectory"""
        try:
            contents = os.listdir(self.current_path)
            selected_element = contents[index]
            full_path = os.path.join(self.current_path, selected_element)

            if os.path.isdir(full_path):
                self.current_path = full_path
                self.display_directory_contents()
            else:
                print(f"Cannot open file {selected_element}")
        except Exception as e:
            print(f"Navigation error: {e}")

    def go_to_parent_directory(self):
        """Move to the parent directory"""
        self.current_path = os.path.dirname(self.current_path)
        self.display_directory_contents()

    def copy_files(self, destination):
        """Copy selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            if not selected_files:
                print("No files selected")
                return

            always_ignore = False
            for file_path in selected_files:
                if os.path.isfile(file_path):
                    if os.path.isdir(destination):
                        dest_path = os.path.join(destination, os.path.basename(file_path))
                    else:
                        dest_path = destination
                        parent_dir = os.path.dirname(dest_path)
                        if parent_dir and not os.path.exists(parent_dir):
                            os.makedirs(parent_dir)
                    
                    try:
                        shutil.copy2(file_path, dest_path)
                    except Exception as e:
                        if not always_ignore:
                            print(f"Copy error for {file_path}: {e}")
                            choice = self.ui.error_choice
                            if choice == 0:  # Ignore once
                                continue
                            elif choice == 1:  # Always ignore
                                always_ignore = True
                                continue
                            elif choice == 2:  # Stop
                                return
            
            print(f"{len(selected_files)} file(s) processed")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Copy error: {e}")

    def move_files(self, destination):
        """Move selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            if not selected_files:
                print("No files selected")
                return

            always_ignore = False
            for file_path in selected_files:
                if os.path.isfile(file_path):
                    if os.path.isdir(destination):
                        dest_path = os.path.join(destination, os.path.basename(file_path))
                    else:
                        dest_path = destination
                        parent_dir = os.path.dirname(dest_path)
                        if parent_dir and not os.path.exists(parent_dir):
                            os.makedirs(parent_dir)
                    
                    try:
                        shutil.move(file_path, dest_path)
                    except Exception as e:
                        if not always_ignore:
                            print(f"Move error for {file_path}: {e}")
                            choice = self.ui.error_choice
                            if choice == 0:  # Ignore once
                                continue
                            elif choice == 1:  # Always ignore
                                always_ignore = True
                                continue
                            elif choice == 2:  # Stop
                                return
            
            print(f"{len(selected_files)} file(s) processed")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Move error: {e}")

    def delete_files(self):
        """Delete selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            if not selected_files:
                print("No files selected")
                return

            files_to_delete = list(selected_files)
            always_ignore = False
            for file_path in files_to_delete:
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        if not always_ignore:
                            print(f"Delete error for {file_path}: {e}")
                            choice = self.ui.error_choice
                            if choice == 0:  # Ignore once
                                continue
                            elif choice == 1:  # Always ignore
                                always_ignore = True
                                continue
                            elif choice == 2:  # Stop
                                return
            
            print(f"{len(files_to_delete)} file(s) processed")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Delete error: {e}")


def main_menu():
    # In a real application, we would use an interactive UI
    ui = MockUI()
    file_manager = FileManager(ui=ui)

    while True:
        print("\n--- File Explorer ---")
        print("1. Display Directory")
        print("2. Navigate")
        print("3. Go to Parent Directory")
        print("4. Select Files")
        print("5. Copy")
        print("6. Move")
        print("7. Delete")
        print("8. Quit")

        choice = input("Your choice: ")

        try:
            if choice == '1':
                file_manager.display_directory_contents()

            elif choice == '2':
                index = int(input("Enter navigation index: "))
                file_manager.navigate(index)

            elif choice == '3':
                file_manager.go_to_parent_directory()

            elif choice == '4':
                file_manager.display_directory_contents()
                indices = input("Enter file indices to select (comma-separated): ")
                file_manager.file_selector.select_files_by_indices(indices, file_manager.current_path)

            elif choice == '5':
                dest = input("Enter destination path for copying: ")
                file_manager.copy_files(dest)

            elif choice == '6':
                dest = input("Enter destination path for moving: ")
                file_manager.move_files(dest)

            elif choice == '7':
                file_manager.delete_files()

            elif choice == '8':
                print("Goodbye!")
                break

            else:
                print("Invalid choice")

        except Exception as e:
            print(f"An error occurred: {e}")


class MockUI(UserInterface):
    """Simple UI for demonstration or test that prompts for error choice"""
    @property
    def error_choice(self):
        while True:
            try:
                print("\nAn error occurred during the operation.")
                print("0. Ignore and continue")
                print("1. Always ignore")
                print("2. Stop operation")
                choice = int(input("Your choice: "))
                if 0 <= choice <= 2:
                    return choice
            except ValueError:
                pass
            print("Invalid choice. Please enter 0, 1, or 2.")


if __name__ == "__main__":
    # In a real app, we might pass a more interactive UI
    main_menu()