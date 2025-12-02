class GithubUser:
    def __init__(self,data):
        self.username = data.get("login")
        self.name = data.get("name")
        self.followers = data.get("followers")
        self.following = data.get("following")
        self.public_repos = data.get("public_repos")
        self.bio = data.get("bio")
        self.avatar = data.get("avatar_url")
        self.created_at = data.get("created_at")


    def summary(self):
        return {
                "Username" : self.username,       
                "Name" : self.name,       
                "Followers" : self.followers,
                "Following" : self.following,
                "Public Repos" : self.public_repos,
                "Bio" : self.bio,
                "Avatar" : self.avatar,
                "Created_At" : self.created_at
            }
