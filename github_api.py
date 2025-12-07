# uses https requests to fetch user info (repos and personal)

import requests

class GithubAPI:
    Base_Url = "https://api.github.com/users/"
    
    def get_user(self,username):
        url = f"{self.Base_Url}{username}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_repos(self,username):
        url = f"{self.Base_Url}{username}/repos?per_page=100"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
