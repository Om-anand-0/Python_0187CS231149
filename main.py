from github_api import GithubAPI
from user import GithubUser
from repo import Repo
from analyzer import Analyzer
from ai.ai_rater import AIRater

from rich import print
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table


def print_user_summary(user):
    table = Table(title="👤 USER SUMMARY", expand=True, show_lines=True)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="bold white")

    for key, value in user.summary().items():
        table.add_row(str(key), str(value))

    print(table)


def print_language_breakdown(stats):
    table = Table(title="🌐 LANGUAGE BREAKDOWN", expand=True, show_lines=True)
    table.add_column("Language", style="bold yellow")
    table.add_column("Count", style="bold white")

    for lang, count in stats.items():
        table.add_row(str(lang), str(count))

    print(table)


def print_repo_summary(repo):
    if not repo:
        print("[bold red]No repositories found[/bold red]")
        return

    table = Table(title="⭐ TOP REPOSITORY", expand=True, show_lines=True)
    table.add_column("Field", style="bold green")
    table.add_column("Value", style="bold white")

    for key, value in repo.summary().items():
        table.add_row(str(key), str(value))

    print(table)


def main():
    username = input("Enter GitHub username: ")

    api = GithubAPI()

    print(Panel.fit(f"🔍 Fetching GitHub data for [bold cyan]{username}[/bold cyan]"))

    # Fetch user
    user_data = api.get_user(username)
    user = GithubUser(user_data)

    # Fetch repos
    repo_data = api.get_repos(username)
    repos = [Repo(r) for r in repo_data]

    analyzer = Analyzer(repos)

    # Display summary
    print_user_summary(user)

    # Display language stats
    print_language_breakdown(analyzer.count_languages())

    # Total stars
    print(Panel.fit(f"⭐ TOTAL STARS: [bold yellow]{analyzer.total_stars()}[/bold yellow]"))

    # Top repo
    print_repo_summary(analyzer.top_repo())

    # AI PROFILE RATING
    print(Panel.fit("🤖 [bold magenta]AI PROFILE RATING[/bold magenta]"))

    ai_profile_rating = AIRater.rate_user_profile(
        user.summary(),
        {
            "total_stars": analyzer.total_stars(),
            "top_repo": analyzer.top_repo().summary() if analyzer.top_repo() else None
        },
        analyzer.count_languages()
    )

    print(Pretty(ai_profile_rating))

    # AI REPO RATINGS
    print(Panel.fit("📂 [bold magenta]AI REPO RATINGS[/bold magenta]"))
    ai_repo_ratings = AIRater.rate_repos(repos)
    print(Pretty(ai_repo_ratings))


if __name__ == "__main__":
    main()

