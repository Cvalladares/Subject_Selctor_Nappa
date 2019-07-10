import json
import sys
import logging
import os
from github import Github
import pandas as pd


# Generate your API Token Via Github
username = 'cvalladares'
password = 'Cmovg@01.'

g = Github(username, password)

headers = {
    'Accept': 'application/vnd.github.v3+json'
}

data = pd.read_csv('repos_randomized.csv', usecols=['owner:string', 'name:string'])

# Open a File to hold all repository URLs
valid_candidates = open("candidates.txt", 'a+')

