import networkx as nx
import matplotlib.pyplot as plt


class GitCodeOwnersMindMap:
    def __init__(self, codeowners_file):
        self.codeowners_file = codeowners_file
        self.path_owners = self.parse_codeowners_file()
        self.mind_map = self.build_mind_map()

    def parse_codeowners_file(self):
        path_owners = {}
        with open(self.codeowners_file, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    path, owners = line.strip().split(' ', 1)
                    owners = owners.split()
                    path_owners[path] = owners
        return path_owners

    def build_mind_map(self):
        G = nx.Graph()
        for path, owners in self.path_owners.items():
            for owner in owners:
                G.add_edge(path, owner)
        return G

    def visualize_mind_map(self):
        pos = nx.spring_layout(self.mind_map)
        nx.draw(self.mind_map, pos, with_labels=True,
                node_color='lightblue', node_size=500, font_size=8)
        plt.show()


# Example usage:
codeowners_file = 'CODEOWNERS'
git_mind_map = GitCodeOwnersMindMap(codeowners_file)
git_mind_map.visualize_mind_map()
