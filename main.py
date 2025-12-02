from github_api import GithubAPI
from user import GithubUser
from repo import Repo
from analyzer import Analyzer

def main():
    username = input("Enter GitHub username: ")

    api = GithubAPI()

    print("\nFetching user info...")
    user_data = api.get_user(username)
    user = GithubUser(user_data)

    print("\nFetching repos...")
    repo_data = api.get_repos(username)
    repos = [Repo(r) for r in repo_data]

    analyzer = Analyzer(repos)

    print("\n===== USER SUMMARY =====")
    print(user.summary())

    print("\n===== LANGUAGE BREAKDOWN =====")
    print(analyzer.count_languages())

    print("\n===== TOTAL STARS =====")
    print(analyzer.total_stars())

    top = analyzer.top_repo()
    if top:
        print("\n===== TOP REPOSITORY =====")
        print(top.summary())

if __name__ == "__main__":
    main()

