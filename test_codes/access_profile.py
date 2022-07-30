import os
import requests
from pprint import pprint

repo_link = str(input("Enter link of repository: "))
temp_list = repo_link.split('/')
repo_site = temp_list[2]

def find_wt_avg(contributors):
    total_contributions=0
    total_followers=0
    total_public_repo=0
    for contributor in contributors:
        user_data = f"https://api.github.com/users/"+contributor[0]
        user_data_json = requests.get(user_data).json()
        total_followers += user_data_json['followers'] * contributor[1]
        total_public_repo+= user_data_json['public_repos'] * contributor[1]
        total_contributions += contributor[1]
    
    weighted_followers = total_followers/total_contributions
    weighted_public_repo = total_public_repo/total_contributions
    return [weighted_followers, weighted_public_repo]



if(repo_site == "github.com"):
    username= temp_list[3]
    print("username: " + username)
    repo_data = f"https://api.github.com/search/repositories?q="+username+'/'+temp_list[4]
    repo_data_json = requests.get(repo_data).json()
    pprint(repo_data_json)

    contribut = f'https://api.github.com/repos/'+username+'/'+temp_list[4]+'/contributors'
    contribut_json = requests.get(contribut).json()
    #pprint(contribut_json)
    
    contributors =[]                #Name of collaborator and their contribution
    for i in range(len(contribut_json)):
        contributors.append([contribut_json[i]['login'], contribut_json[i]['contributions']])
    print(contributors)
    temp = find_wt_avg(contributors)
    weighted_followers, weighted_public_repo = temp[0], temp[1]

    if(repo_data_json['items'][0]['stargazers_count']>300 or weighted_public_repo>50):
        print("It is quiet safe")
    elif(repo_data_json['items'][0]['stargazers_count']>40 or weighted_public_repo>15):
        print("Moderate risky")
    else:
        print("Very Risky")

elif(repo_site == "pypi.org"):
    print("To do")