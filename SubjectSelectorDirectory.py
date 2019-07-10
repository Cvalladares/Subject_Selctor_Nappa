import sys
import shutil
import os
import re
import pandas as pd
from pathlib import Path
import CriteriaTester

repos_directories = os.listdir('../Repos/Repos')

valid_list = list()
valid_repo_url = {"Repo_Url": "Num_Activities"}

for directory in repos_directories:

    # Get all gradle files
    for file in Path('../Repos/Repos/' + directory).glob('**/build.gradle'):
        try:
            file_conents = file.read_text()
            print('Repo Directory: {0}\t'.format(file))
            if CriteriaTester.passes_all_inclusion_criteria(file_conents) and \
                    CriteriaTester.contains_no_exclusion_criteria(file_conents):
                # Only Consider Activities containing a Manifest File
                valid_list.append(file)
                for manifest_file in Path('../Repos/Repos/' + directory).glob('**/AndroidManifest.xml'):
                    print('VALID! ')
                    valid_list.append(file)
                    contents = manifest_file.read_text()
                    activities = re.compile("<\s*activity", re.DOTALL).findall(contents).__len__()
                    valid_repo_url["https://github.com/" + directory.replace("_", "/")] = [activities]
        except:
            print("Error")
            print(sys.exc_info()[0])

downloaded_repos = pd.DataFrame(valid_list)
downloaded_repos.to_csv(os.path.abspath(".\\selected_reps.csv"))

activity_counts = pd.DataFrame.from_dict(valid_repo_url, orient='index')
activity_counts.to_csv(os.path.abspath(".\\activity_counts.csv"))
