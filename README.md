# GitHub Commits

## About:
gitHubCommits is a python program that searches GitHub's public repos and/or specific repos for a given user's last 60 commits. The program writes the output to a csv file in the current working directory and calculates the mean time of commits.

## Contents
Introduction

Installation

How to execute?

Input

Output


## Introduction
This program will pull last 60 commits of a given user from GitHub, using GitHub's search/commit API (https://docs.github.com/en/rest/reference/search#search-commits). Search for commits will be performed on the "default" branch of a repo. If a specific repo is entered as a parameter, commits will be searched within the repo given that user has access.
If no "repo" is passed as a parameter, search for commit happens on all of GitHub's public repos + private repos to which the user has access to

## Installation
- This python program requires the following libraries, Install via the terminal/command prompt using the below commands

```
- pip install requests
- pip install pathlib
- pip install os
- pip install csv
- pip install pandas
- pip install numpy
- pip install math
```
- GitHub Personal Access token
https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

## How to execute?
 - This python program needs to be executed from your IDE's (https://realpython.com/python-ides-code-editors-guide/#python-specific-editors-and-ides)
 
## Input
 This program accepts three inputs via console
  - GitHub username
  - GitHub Personal access token
  - Github Repo (Username/Repo or ORG/Repo) (optional, if commits for a specific repo is required)

## Output
 This program generates two types of output 
 - csv file in the current working directory with the input GitHub user name as file name (<GitHubUser>.csv)
 - Prints mean commit time of the last 60 commits in Days, Hours & Minutes format (Console print)
  (Ex: For example, if User A only had 3 commits in their history on one day at 8am, 11am, and 4pm, the time between the commits are 3 hours and 5 hours. So User A's mean time between commits would be 4 hours. (3+5)/2)
 
  
