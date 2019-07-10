import simplejson
import requests
import base64
import pandas as pd
import CriteriaTester

# Generate your API Token Via Github
username = 'cvalladares'
api_token = 'a86e5a1fb5b0761779770ae1e26442a256967433'
api_url_base = 'https://api.github.com/'

headers = {
    'Accept': 'application/vnd.github.v3+json'
}

data = pd.read_csv('repos_randomized.csv', usecols=['owner:string', 'name:string'])
data.to_excel("")
# Open a File to hold all repository URLs
valid_candidates = open("candidates.txt", 'a+')

for owner, repo in data.values:
    # Find all build.gradle files from the repository
    payload_build_search = {'q': 'repo:' + owner + '/' + repo + '+filename:build+extension:gradle'}
    # Concatenate all key-value pairs to prevent the URL encoding from taking place
    # (Github does not use percent encoding)
    payload_str = "&".join("%s=%s" % (k, v) for k, v in payload_build_search.items())

    # The API endpoint to determine where a file code resides
    url_base_file_search = api_url_base + 'search/code'

    resp = requests.get(url_base_file_search,
                        headers=headers,
                        params=payload_str,
                        auth=(username, api_token))

    # If the file has been found
    if resp.status_code == 200:
        data = resp.json()

        for item in data['items']:
            # Find the path in which the build file resides
            path = item['path']

            # Endopoint to download the build file
            url_content_fetch = 'https://api.github.com/repos/' + owner + '/' + repo + '/contents/' + path
            res_content_req = requests.get(url_content_fetch,
                                           headers=headers,
                                           auth=(username, api_token))

            # If the build fild would be downloaded
            if res_content_req.status_code == 200:
                build_file_json = res_content_req.json()

                # Parse JSON and get the contents
                build_file_encoded_contents = build_file_json['content']
                # Decode the contents
                build_file_decoded_contents = base64.b64decode(build_file_encoded_contents).decode('utf-8')

                print('Owner: {0}\tRepo: {1}\t'.format( owner, repo), end=' ')
                if CriteriaTester.passes_all_inclusion_criteria(build_file_decoded_contents) and \
                        CriteriaTester.contains_no_exclusion_criteria(build_file_decoded_contents):
                    print('VALID! URL: '.format(owner,repo,item['repository']['html_url']))
                    valid_candidates.write('%s\n' % item['repository']['html_url'])

    elif resp.status_code == 422:
        continue


    # As soon as an error code is thrown by the API terminate
    else:
        valid_candidates.close()
        exit(22)
