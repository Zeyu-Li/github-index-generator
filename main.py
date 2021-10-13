import requests
import math
import json
import re

GITHUB_USERNAME = "Zeyu-Li"

def getRepoAPI(file = "data.json"):
    r = requests.get(f'https://api.github.com/users/{GITHUB_USERNAME}')
    try:
        count = r.json()['public_repos']
    except:
        raise Exception("Exceeded API limit")
        return

    repos = []
    for i in range(math.ceil(count/2)):
        r = requests.get(f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&page={i+1}')
        repos += r.json()
    
    # dumps in json just in case
    with open(file, "w") as fp:
        json.dump(repos, fp)

    return repos

def getGistAPI(file = "gist.json"):
    r = requests.get(f'https://api.github.com/users/{GITHUB_USERNAME}/gist')
    gists = r.json()
    
    # dumps in json just in case
    with open(file, "w") as fp:
        json.dump(gists, fp)

    return gists


def getRepoFile(file = "data.json"):
    with open(file, "r", encoding="utf-8") as fp:
        return json.loads(fp.read())

def getGistFile(file = "gist.json"):
    with open(file, "r", encoding="utf-8") as fp:
        return json.loads(fp.read())

def getReposText(repos):
    returnText = ""
    for repo in repos:
        # homepage = repo['homepage'].replace('https://','') if repo['homepage'] else ''
        # print(returnText)
        returnText += ("* [" + ' '.join(name.title() for name in re.split('; |, |\*|_|-', repo['name'])) + \
        f"]({repo['html_url']}) - {repo['description']}" + (f" [Website @ [{repo['homepage'].replace('https://','') if repo['homepage'] else ''}]({repo['homepage']})]" if repo['homepage'] else '') + '\n')

    return returnText

def getGistsText(gists):
    returnText = ""
    gists.sort(key=lambda a : list(a['files'].keys())[0].lower())
    for gist in gists:
        returnText += (f"* [{list(gist['files'].keys())[0]}]({gist['html_url']}) - {gist['description']}\n")

    return returnText

def main():
    repos = getRepoFile()
    gists = getGistFile()

    template = f"""
# GitHub Index

<a name="top"></a>

<a href="#all">Jump to **All** repos</a>

<a href="#gist">Jump to **Gists**</a>

<a name="all_r"></a>

## ({len(repos)}) All GitHub Repos

{getReposText(repos)}

<a name="gist"></a>

## ({len(gists)}) All Gists

{getGistsText(gists)}

## About

This is a index to all my **GitHub repos**. It acts as a quick-link to all my projects as well as a description to each repo

**<a href="#top">🔝 Back to Top</a>**
"""

    with open("README.md", "w", encoding="utf-8") as fp:
        fp.writelines(template)

    return 0

if __name__ == "__main__":
    main()
