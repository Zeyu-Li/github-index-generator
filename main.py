import requests
import math
import json
import re

GITHUB_USERNAME = "Zeyu-Li"
FILES = False
REPOS_FILE = "data.json"
GISTS_FILE = "gists.json"

def getReposAPI(file = f"{REPOS_FILE}"):
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
    
    # clean up
    repos = list(filter(lambda x: not (x == "message" or x == "documentation_url"), repos))

    # dumps in json just in case
    with open(file, "w") as fp:
        json.dump(repos, fp)

    return repos

def getGistsAPI(file = f"{GISTS_FILE}"):
    r = requests.get(f'https://api.github.com/users/{GITHUB_USERNAME}/gists')
    gists = r.json()

    return gists


def getRepoFile(file = f"{REPOS_FILE}"):
    with open(file, "r", encoding="utf-8") as fp:
        return list(filter(lambda x: not (x == "message" or x == "documentation_url"), json.loads(fp.read())))

def getGistFile(file = f"{GISTS_FILE}"):
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

def getLanguages(repos):
    # sort by language
    languages = dict()
    for repo in repos:
        returnText = ("* [" + ' '.join(name.title() for name in re.split('; |, |\*|_|-', repo['name'])) + \
        f"]({repo['html_url']}) - {repo['description']}" + (f" [Website @ [{repo['homepage'].replace('https://','') if repo['homepage'] else ''}]({repo['homepage']})]" if repo['homepage'] else '') + '\n')
        if repo['language'] in languages or (repo['language'] == None and "Misc" in languages):
            languages['Misc' if repo['language'] == None else repo['language']] += returnText
        else:
            languages['Misc' if repo['language'] == None else repo['language']] = returnText

    new_line = '\n'
    return ''.join(f"### ({languages[language].count(new_line)}) {language}{new_line + new_line + languages[language] + new_line + new_line}" for language in sorted(languages))


def main():
    FILES = not input("Use API to get repos y/N: ")[0].lower() == 'y'
    repos = getRepoFile() if FILES else getReposAPI()
    gists = getGistFile() if FILES else getGistsAPI()

    if (gists['documentation_url'] == 'https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting'):
        # if API limit reaches, use json file
        gists = getGistFile()

    template = f"""
# GitHub Index

<a name="top"></a>

## About

This is a index to all my **GitHub Repositories**. It acts as a quick-link to all my projects as well as a description to each repo

<a href="#all">Jump to **All Repositories**</a> | <a href="#gist">Jump to **Gists**</a> | <a href="#languages">Jump to **By Languages**</a>

<a name="all_r"></a>

## ({len(repos)}) All GitHub Repos

{getReposText(repos)}


<a name="gist"></a>

## ({len(gists)}) All Gists

{getGistsText(gists)}


<a name="languages"></a>

## By Languages

{getLanguages(repos)}
**<a href="#top">🔝 Back to Top</a>**
"""

    with open("README.md", "w", encoding="utf-8") as fp:
        fp.writelines(template)

    return 0

if __name__ == "__main__":
    main()
