import requests
import os
import json

ORG_NAME = "galaxi67"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

def get_repos():
    url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=100"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_languages(repo_name):
    url = f"https://api.github.com/repos/{ORG_NAME}/{repo_name}/languages"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def generate_language_stats():
    repos = get_repos()
    language_usage = {}

    for repo in repos:
        languages = get_languages(repo["name"])
        for lang, bytes_used in languages.items():
            language_usage[lang] = language_usage.get(lang, 0) + bytes_used

    sorted_languages = sorted(language_usage.items(), key=lambda x: x[1], reverse=True)

    return sorted_languages

def update_readme():
    languages = generate_language_stats()
    readme_content = "# Most Used Languages in Organization\n\n"
    
    for lang, bytes_used in languages:
        readme_content += f"- {lang}: {bytes_used} bytes\n"

    with open("README.md", "w") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
