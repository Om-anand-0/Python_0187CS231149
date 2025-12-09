# perfoms calculation (stars repos and stuff)

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
        if not self.repos:
            return None
        return max(self.repos, key=lambda r: r.stars, default=None or 0)
    
    def repo_lang_raw(self):
        return [repo.raw_json.get("language") for repo in self.repos]

