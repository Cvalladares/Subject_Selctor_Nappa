from github import Github
import pandas as pd
from datetime import datetime, timedelta
import re
import sys
import os

g = Github("cvalladares", "Cmovg@01.")
data = pd.read_csv('activity_counts.csv', usecols=['Repo_Url', 'Num_Activities'])
reps_by_last_commit = {'Repo_Url', 'Num_Activities', }
updated_repos = list()

for Repo_Url, Num_Activities in data.values:
    try:
        number_of_activities = int(Num_Activities.replace('[', '').replace(']', ''), 10)
        if number_of_activities > 3:
            owner_repo_chunk = re.compile("https://github.com/").split(Repo_Url)
            repo = g.get_repo(owner_repo_chunk[1])
            since = datetime.now() - timedelta(days=800)
            commits = repo.get_commits(since=since)
            for commit in commits:
                if commit.commit.author.date > since:
                    updated_repos.append(Repo_Url)
                    break
    except:
        print(sys.exc_info()[0])



valid_repos = pd.DataFrame(updated_repos)
valid_repos.to_csv(os.path.abspath(".\\newer_repos.csv"))
