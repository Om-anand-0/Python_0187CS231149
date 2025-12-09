# initializes repo info to repo objects and made a func to return user summary


class Repo:
    def __init__(self, data:dict):
        self.raw_json = data
        
        self.name = data.get("name")
        self.language = data.get("language")
        self.stars = data.get("stargazers_count")
        self.forks = data.get("forks_count")
        self.size = data.get("size")

    def summary(self):
        return {
            "name": self.name,
            "language": self.language,
            "stars": self.stars,
            "forks": self.forks,
            "size_kb": self.size
        }

    def show_raw_json(self):
        return self.raw_json