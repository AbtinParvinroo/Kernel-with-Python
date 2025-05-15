class FileSystem:
    def __init__(self):
        self.fs = {"": {}}

    def _traverse(self, path, create_missing=False):
        parts = [part for part in path.strip("/").split("/") if part]
        current = self.fs[""]
        for part in parts[:-1]:
            if part not in current:
                if create_missing:
                    current[part] = {}
                else:
                    return None, None
            current = current[part]
            if not isinstance(current, dict):
                return None, None
        final = parts[-1] if parts else ""
        return current, final

    def create_file(self, path, content):
        parent, filename = self._traverse(path, create_missing=True)
        if parent is None:
            print(f"[FS] Error: Invalid path '{path}'.")
            return False
        if filename in parent:
            print(f"[FS] Error: File or directory '{filename}' already exists.")
            return False
        parent[filename] = content
        print(f"[FS] File '{path}' created.")
        return True

    def read_file(self, path):
        parent, filename = self._traverse(path)
        if parent is None or filename not in parent:
            print(f"[FS] File '{path}' not found.")
            return None
        if isinstance(parent[filename], dict):
            print(f"[FS] '{path}' is a directory, not a file.")
            return None
        print(f"[FS] Reading file '{path}':")
        print(parent[filename])
        return parent[filename]

    def write_file(self, path, content):
        parent, filename = self._traverse(path)
        if parent is None or filename not in parent:
            print(f"[FS] File '{path}' not found.")
            return False
        if isinstance(parent[filename], dict):
            print(f"[FS] '{path}' is a directory, not a file.")
            return False
        parent[filename] = content
        print(f"[FS] File '{path}' updated.")
        return True

    def delete_file(self, path):
        parent, filename = self._traverse(path)
        if parent is None or filename not in parent:
            print(f"[FS] File '{path}' not found.")
            return False
        if isinstance(parent[filename], dict):
            print(f"[FS] '{path}' is a directory, not a file.")
            return False
        del parent[filename]
        print(f"[FS] File '{path}' deleted.")
        return True

    def create_directory(self, path):
        parent, dirname = self._traverse(path, create_missing=True)
        if parent is None:
            print(f"[FS] Error: Invalid path '{path}'.")
            return False
        if dirname in parent:
            print(f"[FS] Error: Directory or file '{dirname}' already exists.")
            return False
        parent[dirname] = {}
        print(f"[FS] Directory '{path}' created.")
        return True

    def list_directory(self, path):
        if path == "/" or path == "":
            directory = self.fs[""]
        else:
            parent, dirname = self._traverse(path)
            if parent is None or dirname not in parent:
                print(f"[FS] Directory '{path}' not found.")
                return None
            directory = parent[dirname]
            if not isinstance(directory, dict):
                print(f"[FS] '{path}' is not a directory.")
                return None
        print(f"[FS] Listing contents of '{path}':")
        for name in directory:
            type_name = "Directory" if isinstance(directory[name], dict) else "File"
            print(f"  {name} ({type_name})")
        return directory

    def rename_item(self, old_path, new_path):
        old_parent, old_name = self._traverse(old_path)
        if old_parent is None or old_name not in old_parent:
            print(f"[FS] Item '{old_path}' not found for renaming.")
            return False
        item = old_parent.pop(old_name)
        new_parent, new_name = self._traverse(new_path, create_missing=True)
        if new_parent is None:
            print(f"[FS] Invalid new path '{new_path}'.")
            return False
        if new_name in new_parent:
            print(f"[FS] Cannot rename to '{new_path}'; already exists.")
            return False
        new_parent[new_name] = item
        print(f"[FS] Renamed '{old_path}' to '{new_path}'.")
        return True

    def move_item(self, source_path, destination_path):
        source_parent, source_name = self._traverse(source_path)
        if source_parent is None or source_name not in source_parent:
            print(f"[FS] Source item '{source_path}' not found.")
            return False
        item = source_parent.pop(source_name)
        dest_parent, dest_name = self._traverse(destination_path, create_missing=True)
        if dest_parent is None:
            print(f"[FS] Invalid destination path '{destination_path}'.")
            return False
        if dest_name in dest_parent:
            print(f"[FS] Destination '{destination_path}' already exists.")
            return False
        dest_parent[dest_name] = item
        print(f"[FS] Moved '{source_path}' to '{destination_path}'.")
        return True

    def delete_directory(self, path, recursive=False):
        parent, dirname = self._traverse(path)
        if parent is None or dirname not in parent:
            print(f"[FS] Directory '{path}' not found.")
            return False
        if not isinstance(parent[dirname], dict):
            print(f"[FS] '{path}' is not a directory.")
            return False
        if parent[dirname] and not recursive:
            print(f"[FS] Directory '{path}' is not empty. Use recursive delete to remove it.")
            return False
        del parent[dirname]
        print(f"[FS] Directory '{path}' deleted{' recursively' if recursive else ''}.")
        return True

    def get_info(self, path):
        if path == "/" or path == "":
            item = self.fs[""]
            item_type = "Directory"
        else:
            parent, name = self._traverse(path)
            if parent is None or name not in parent:
                print(f"[FS] Item '{path}' not found.")
                return None
            item = parent[name]
            item_type = "Directory" if isinstance(item, dict) else "File"
        print(f"[FS] Info for '{path}': Type: {item_type}")
        return {"path": path, "type": item_type}

if __name__ == "__main__":
    fs = FileSystem()

    fs.create_directory("/docs")
    fs.create_file("/docs/readme.txt", "Welcome to the minimal file system!")
    fs.create_directory("/docs/tutorials")
    fs.create_file("/docs/tutorials/lesson1.txt", "This is lesson 1.")

    fs.list_directory("/docs")

    fs.read_file("/docs/readme.txt")

    fs.write_file("/docs/readme.txt", "Updated content of readme.")
    fs.read_file("/docs/readme.txt")

    fs.rename_item("/docs/readme.txt", "/docs/introduction.txt")
    fs.list_directory("/docs")

    fs.move_item("/docs/introduction.txt", "/docs/tutorials/introduction.txt")
    fs.list_directory("/docs/tutorials")

    fs.delete_file("/docs/tutorials/lesson1.txt")
    fs.list_directory("/docs/tutorials")

    fs.create_directory("/projects")
    fs.create_file("/projects/project1.txt", "Project 1 details.")
    fs.list_directory("/projects")

    fs.get_info("/docs")
    fs.get_info("/projects/project1.txt")

    fs.delete_directory("/projects", recursive=False)

    fs.create_directory("/projects")
    fs.create_file("/projects/project2.txt", "Project 2 details.")
    fs.list_directory("/projects")

    fs.delete_directory("/docs/tutorials", recursive=True)
    fs.list_directory("/docs")