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
    

def main():
    username = input("Enter Github Username :")

    api = GithubAPI()
    user_data = api.get_user(username)
    #user = GithubUser(user_data)
    
    repo_data = api.get_repos(username)
    repo_count = len(repo_data)
    repo_names = [r["name"] for r in repo_data]
    print(repo_names) 
    print("number of repos are : ", repo_count)

if __name__ == "__main__":
    main()
