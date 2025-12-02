from collections import Counter

class Analyzer:
    def __init__(self, repos):
        self.repos = repos

    def count_languages(self):
        langs = [repo.language for repo in self.repos if repo.language]
        return Counter(langs)

    def total_stars(self):
        return sum(repo.stars for repo in self.repos)

    def top_repo(self):
        return max(self.repos, key=lambda r: r.stars, default=None)

