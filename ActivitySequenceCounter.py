from collections import defaultdict
import traceback
import pandas as pd
import functools

import xml.etree.ElementTree as ET
import re
import sys
import os
from pathlib import Path


def DFS(G, v, seen=None, path=None):
    if seen is None: seen = []
    if path is None: path = [v]

    seen.append(v)

    paths = []

    for t in G[v]:
        if t not in seen:
            t_path = path + [t]
            paths.append(tuple(t_path))
            paths.extend(DFS(G, t, seen[:], t_path))
    if not paths:
        paths.append('')

    return paths


repos_directories = os.listdir('../Repos/Repos')

data = pd.read_csv('activity_counts.csv', usecols=['Repo_Url', 'Num_Activities'])

apps_by_activity_length = list()

for Repo_Url, Num_Activities in data.values:
    activity_graph = defaultdict(set)

    try:
        number_of_activities = int(Num_Activities.replace('[', '').replace(']', ''), 10)
        if number_of_activities > 3:
            owner_repo_chunk = re.compile("https://github.com/").split(Repo_Url)
            directory = '../Repos/Repos/' + owner_repo_chunk[1].replace("/", "_")
            activity_list = list()
            main_activity_handle = None
            main_activity_name = None
            for manifest_file in Path(directory).glob('**/AndroidManifest.xml'):

                contents = manifest_file.read_text()
                root = ET.fromstring(contents)
                for activity in root.iter('activity'):
                    act_name = activity.attrib['{http://schemas.android.com/apk/res/android}name']
                    if act_name is not None:
                        if main_activity_handle is None:
                            for action in activity.iter('action'):
                                temp = action.attrib['{http://schemas.android.com/apk/res/android}name']
                                if temp == 'android.intent.action.MAIN':
                                    main_activity_handle = act_name
                        activity_list.append(act_name)

            for activity in activity_list:

                filename = (activity.split(".")[-1])
                if activity == main_activity_handle:
                    main_activity_name = filename

                try:
                    java_file_contents = next(Path(directory).glob('**/' + filename + '.java')).read_text()
                except StopIteration:
                    pass
                except UnicodeDecodeError:
                    print("Repo {0} in another language".format(Repo_Url))

                line_of_code = re.compile("(new\s+Intent\s*\()(.*\.class)(\s*)").findall(java_file_contents)
                for token in line_of_code:
                    target_class_name = token[1][token[1].rfind(",") + 1:].lstrip()
                    target = target_class_name.split(".")[0]
                    if filename != target:
                        activity_graph[filename].add(target)

                line_of_code = re.compile("(.launchActivity\s*\(.*\.class)(\s*)").findall(java_file_contents)
                for token in line_of_code:
                    target_class_name = token[0][token[0].rfind(",") + 1:].lstrip()
                    target = target_class_name.split(".")[0]
                    if filename != target:
                        activity_graph[filename].add(target)


            all_paths = [p for ps in [DFS(activity_graph, n) for n in set(activity_graph)] for p in ps]
            # path_lengths = DFS(activity_graph, main_activity_name)

            longest_path = functools.reduce(
                lambda a, b: a if len(a) > len(b) else b,
                #path_lengths
                all_paths
            )

            apps_by_activity_length.append(
                (Repo_Url, Num_Activities.replace("[", "").replace("]", ""), len(longest_path),
                 " -> ".join(str(x) for x in longest_path)))

    except:
        print(sys.exc_info())

valid_repos = pd.DataFrame(apps_by_activity_length,
                           columns=('Repo_Url', 'Num_Activities', 'Longest_Activity_Chain_Count',
                                    'Longest_Activity_Chain'))
valid_repos.to_csv(os.path.abspath(".\\newer_repos_all_path.csv"))
