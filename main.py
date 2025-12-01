import requests

class GithubAPI:
    Base_Url = "https://api.github.com/users/"
    
    def get_user(self,username):
        url = f"{self.Base_url}{username}"
        response = requests.get(url)
        response.raise_for_status()
        return respons.json()
    
    def get_repos(self,name):
        url = f"{self.Base_url}{username}/repos?per_page=100"
        response = requests.get(url)
        response.raise_for_status()
        return respons.json()
