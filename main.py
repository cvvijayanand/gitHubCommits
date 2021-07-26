# Pre-requisite libraries
import pathlib
import os
import requests
import csv
import pandas as pd
import numpy as np
import math


# Receive GitHub username, token & Repo to search
def get_user_input():
    git_user_repo = 'NoRepo'
    git_pers_token = 'NoToken'
    git_user_name = input('Enter a valid GitHub user name: ').strip()
    if git_user_name != '':
        git_pers_token = input("Enter your personal access GitHub token: ").strip()
        if git_pers_token == '':
            print('Invalid token, try again')
            exit()
        user_input_repo = input("Search a specific repo: Enter Y, to search all GitHub: Enter 'N': ").upper()
        if user_input_repo == 'Y':
            git_user_repo = input("Enter the repo to be searched ex: USERNAME/Repo: octokit/octokit.rb: ").strip()
        elif user_input_repo == 'N':
            git_user_repo = 'NoRepo'
        else:
            print("Invalid input, Enter a Y/N, try again")
            exit()
    else:
        print("Invalid input, Try again and enter a valid GitHub user name")
        exit()
    return git_user_name, git_user_repo, git_pers_token


# function to receive URL and store last 60 commits in JSON
def get_all_commits(git_url, git_header):
    git_data = ''
    try:
        response = requests.get(git_url, headers=git_header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errhttp:
        print(errhttp)
    except requests.exceptions.ConnectionError as errcon:
        print(errcon)
    except requests.exceptions.Timeout as errtime:
        print(errtime)
    except requests.exceptions.RequestException as errexcep:
        print(errexcep)
    else:
        json_response = response.json()
        git_data = json_response['items']
    return git_data


# Write user's last 60 commits to a csv file
def write_user_commits(git_output_data):
    data_file = open(output_file, 'w')
    csv_writer = csv.writer(data_file)
    file_loc = pathlib.Path(__file__).resolve().parent
    git_data_file = gituser + '.csv'

    header = ['Author', 'Repo', 'Commit_date', 'Commit_URL']
    csv_writer.writerow(header)

    for items in git_output_data:
        extract_committer = items['commit']['committer']
        extract_tmp_date = pd.Timestamp(extract_committer['date'])
        extract_date = extract_tmp_date.tz_convert(tz='EST')
        extract_repo = items['repository']['name']
        extract_author = items['author']['login']
        extract_commit_url = items['commit']['url']
        csv_values = [extract_author, extract_repo, extract_date, extract_commit_url]
        csv_writer.writerow(csv_values)

    data_file.close()
    print("Last 60 commits for entered user are written in the following file:", file_loc / git_data_file)
    return data_file


# Compute mean time between the last 60 commits
def avg_commit_time(file_to_read):
    file = open(file_to_read)
    reader = csv.reader(file)
    lines = len(list(reader))
    if lines > 1:
        data = pd.read_csv(file_to_read, parse_dates=['Commit_date'])
        diff_list = []
        for i in range((lines - 2)):
            diff_list.append(((data['Commit_date'][i]) - (data['Commit_date'][i + 1])).total_seconds())

        avg = round(np.average(diff_list))
        days = math.floor(avg / 86400)
        hours = math.floor((avg % 86400) / 3600)
        minutes = math.floor(((avg % 86400) % 3600) % 60)
        print(f'Total Average commit time in seconds -  {avg}')
        print(f'Average time for commits : {days} days, {hours} hours, {minutes} minutes')
    else:
        print("There are no commits found for the given user, try with another user/repo")
    file.close()


# Initialize variables
url = ''
headers = ''

# Call user input
gituser, gitrepo, gittoken = get_user_input()
token = os.getenv('GITHUB_TOKEN', gittoken)
user_to_check = gituser
repo_to_check = gitrepo

# Validate user input
if gituser != '' and gitrepo != 'NoRepo':
    github_api = 'https://api.github.com/search/commits'
    sort_params = '&per_page=60&sort=committer-date&order=desc'
    query_params = '?q=author:' + user_to_check + '+repo:' + repo_to_check + sort_params
    output_file = gituser + '.csv'
    url = github_api + query_params
elif gitrepo != '' and gitrepo == 'NoRepo':
    github_api = 'https://api.github.com/search/commits'
    query_params = '?q=author:' + user_to_check + '&per_page=60&sort=committer-date&order=desc'
    output_file = gituser + '.csv'
    url = github_api + query_params

# Assign header values
headers = {'Accept': 'application/vnd.github.cloak-preview.json', 'Authorization': f'token {token}'}

# Call function to get last 60 commits
git_hub_data = get_all_commits(url, headers)

# pass the csv file to find mean commit time
if git_hub_data != '':
    write_output_to_csv = write_user_commits(git_hub_data)
    filepath = pathlib.Path(__file__).resolve().parent
    csv_file = gituser + '.csv'
    file_to_compute_mean = filepath / csv_file
    avg_commit_time(file_to_compute_mean)
else:
    print("Your request couldn't be processed due to above error, verify if the GitHub User/Token is valid")
