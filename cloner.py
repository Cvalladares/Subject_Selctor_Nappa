
import sys
import shutil
import os
from git.repo.base import Repo
import pandas as pd

repos_to_clone = './otherData/repos_to_clone.json'
cloned_repos_json = './otherData/cloned_repos.json'
clones_path = '../Repos/'


def get_clone_path(owner, repo, is_absolute):
    if (is_absolute):
        return os.path.abspath(clones_path + "\\Repos\\" + owner + "_" + repo)
    else:
        return clones_path + clones_path + "\\Repos\\" + owner + "_" + repo


def clone_repo(owner, repo, path_to_clone):
    try:
        if (not os.path.exists(path_to_clone)):
            git_url = "https://github.com/" + owner + "/" + repo
            Repo.clone_from(url=git_url, to_path=path_to_clone)
        else:
            print("Jumped repo because its folder already exists: " + repo['id'])
    except:
        print("Error for: Owner -- {0} Repo -- {1}".format(owner, repo))
        print(sys.exc_info()[0])
        # Delete clones that fail
        #shutil.rmtree(path_to_clone, ignore_errors=False, onerror=None)


def start_cloning():
    data = pd.read_csv('repos_randomized.csv', usecols=['owner:string', 'name:string'])
    counter = 1
    cloned_repos = list()
    downloaded_repos_dir = os.path.abspath(".\\downloaded_repos.csv")

    for owner, repo in data.values:
        print("Cloning repo number " + str(counter) + " --- " + owner + "/" + repo)
        counter += 1
        absolute_path_to_clone = get_clone_path(owner=owner, repo=repo, is_absolute=True)
        clone_repo(owner, repo, absolute_path_to_clone)
        cloned_repos.append(absolute_path_to_clone)
        if counter == 3500:
            break

    downloaded_repos = pd.DataFrame(cloned_repos)
    downloaded_repos.to_csv(downloaded_repos_dir)


start_cloning()
