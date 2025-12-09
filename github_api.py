# uses https requests to fetch user info (repos and personal)

import requests
import logging
from functools import wraps

logging.basicConfig(
    filename="github_analyzer.log",
    level=logging.INFO,
    filemode="a",
    format="%(asctime)s - %(message)s"
)

logger = logging.getLogger("GithubAnalyzer")

def log_api_call(func): 
    @wraps(func)
    def wrapper(*args,**kwargs):
        logger.info(f"calling API Function: {func.__name__}")
        try:
            result = func(*args,**kwargs)
            logger.info(f"{func.__name__} worked")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed, Error is {str(e)}")
            raise
    return wrapper



class GithubAPI:
    Base_Url = "https://api.github.com/users/"
    headers = {"User-Agent": "Github-User-Analyzer"}
    
    @log_api_call
    def get_user(self,username):
        url = f"{self.Base_Url}{username}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    @log_api_call
    def get_repos(self,username):
        url = f"{self.Base_Url}{username}/repos?per_page=100"
        response = requests.get(url,headers=self.headers)
        response.raise_for_status()
        return response.json()
    
