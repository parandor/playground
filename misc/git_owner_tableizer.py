import os
import pandas as pd


class GitCodeOwnersTable:
    def __init__(self, codeowners_file, repo_path, num_levels=3):
        self.codeowners_file = codeowners_file
        self.repo_path = repo_path
        self.path_owners = self.parse_codeowners_file()
        self.path_table = self.create_path_table(num_levels)

    def parse_codeowners_file(self):
        path_owners = {}
        with open(self.codeowners_file, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    path, owners = line.strip().split(' ', 1)
                    owners = owners.split()
                    path_owners[path] = owners
        return path_owners

    def create_path_table(self, num_levels):
        path_table = {}
        for root, dirs, files in os.walk(self.repo_path):
            depth = root[len(self.repo_path) + len(os.path.sep):].count(os.path.sep)
            if depth > num_levels:
                continue
            for file in files:
                if file == 'CODEOWNERS':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                parts = line.split()
                                if len(parts) > 1:
                                    path = parts[0].strip('/')
                                    owners = [owner.strip()
                                              for owner in parts[1:]]
                                    if path not in path_table:
                                        path_table[path] = set()
                                    path_table[path].update(owners)
        return path_table

    def visualize_path_table(self):
        path_list = []
        owner_list = []
        for path, owners in self.path_table.items():
            if owners:
                path_list.append(path)
                owner_list.append(', '.join(owners))
        data = {'Path': path_list, 'Assigned Owners': owner_list}
        df = pd.DataFrame(data)
        print(df)


# Example usage:
codeowners_file = 'CODEOWNERS'
repository_directory = '/home/peter/myrepo'
git_code_owners_table = GitCodeOwnersTable(
    codeowners_file, repository_directory, 2)
git_code_owners_table.visualize_path_table()
