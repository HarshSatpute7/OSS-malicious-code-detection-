import os
import requests
from pprint import pprint
import shutil, stat
import yara
from git.repo.base import Repo

#The extensions of files which should be scanned
valid_extensions = {'.c', '.cpp', '.py', '.java', '.m', '.html', '.css', '.js', '.sh', '.r', '.php', '.xhtml', '.net'} 
#Name on files who don't have an extension 
invalid_files = {".git", ".gitignore", ".gitattributes", ".classpath", ".project", "LICENSE"} 

#Loading pre-compiled YARA rulesg
rules = yara.load("./compiled_yara_rules/final_compiled") 


def find_wt_avg(contributors):                      #Function to calculate weighted public repository count and followers
    total_contributions=0                           #Declaring total to 0
    total_followers=0
    total_public_repo=0

    #Weighted count of followers will be a contributors followers*his contribution/total contributions
    #Similarly for weighted public repository. The task of dividing is donw at end
    for contributor in contributors:                #Calculating total
        user_data = f"https://api.github.com/users/"+contributor[0]
        user_data_json = requests.get(user_data).json()
        total_followers += user_data_json['followers'] * contributor[1]
        total_public_repo+= user_data_json['public_repos'] * contributor[1]
        total_contributions += contributor[1]
    
    weighted_followers = total_followers/total_contributions            #Calculating weighted followers and public_repo
    weighted_public_repo = total_public_repo/total_contributions
    return [weighted_followers, weighted_public_repo]                   #Returning values


def download_repo(repo_link):                       #Function to clone a github repository
    #repo_path = "D:/FlipKart_GRID/H1N1/repo_download"
    repo_path = "./repo_download"                   #Declaring a path to store

    for root, dirs, files in os.walk(repo_path):    #Deleting previous files inside repo_path
        for fname in files:
            full_path = os.path.join(root, fname)
            os.chmod(full_path ,stat.S_IWRITE)
            os.remove(full_path)

    #os.chmod(repo_path ,stat.S_IWRITE)
    shutil.rmtree(repo_path)

    Repo.clone_from(repo_link, repo_path)           #Cloning the repository using git
    print("Repository cloned successfully!")


def access_profile(repo_link):                      #Function to check profile
    temp_list = repo_link.split('/')                #Spliting at / to get website, username and repo name
    repo_site = temp_list[2]

    if(repo_site == "github.com"):                  #Only if it is a github link profile can be verified
        username= temp_list[3]
        print("Username: " + username)              #Printing username
        #Calling Github API to get data about repository
        repo_data = f"https://api.github.com/search/repositories?q="+username+'/'+temp_list[4]      
        repo_data_json = requests.get(repo_data).json()
        #pprint(repo_data_json)

        #Calling Github API to get contributors of that repository
        contribut = f'https://api.github.com/repos/'+username+'/'+temp_list[4]+'/contributors'
        contribut_json = requests.get(contribut).json()
        #pprint(contribut_json)
        
        contributors =[]                            #Name of contributor and their contribution is stored in list
        for i in range(len(contribut_json)):
            contributors.append([contribut_json[i]['login'], contribut_json[i]['contributions']])
        print(contributors)                         #Displayign name and contributons of contributors
        temp = find_wt_avg(contributors)            #Calculating weighted followers and weighted public repoitories
        
        weighted_followers, weighted_public_repo = temp[0], temp[1]     

        #Distinguishing autheticness based on star count of repository and weighted public repo of contributors
        if(repo_data_json['items'][0]['stargazers_count']>300 or weighted_public_repo>50):
            print("Using this repository is safe")
        elif(repo_data_json['items'][0]['stargazers_count']>40 or weighted_public_repo>15):
            print("Using this repository is a bit risky")
        else:
            print("Using this repository is risky")
        
        download_repo(repo_link)                    #Downloading the github repository


def check(repo_path):                               #Function to check if its a code file and test against yara rules
    global valid_extensions, invalid_files, rules
    for f in os.listdir(repo_path):                 #Travering the folder
        dir = os.path.join(repo_path, f)

        file_name, file_extension = os.path.splitext(dir)
        #print(file_name, file_extension, f)
        if(file_extension in valid_extensions):     #If it's a code file
            matches = rules.match(dir)
            print(f + " contains : ", end="")
            print(matches)
        #If it's a folder, various times a file named .git gets downloaded with no extension
        if(not file_extension and f not in invalid_files):      #To traverse inside folder in heirarchial manner
            check(file_name)


def test_yara():                                    #Function to check against yara
    repo_path = "./repo_download"                   #Declaring path where code files from repo exist
    check(repo_path)                                


#If not a github link enter anything and make sure package is downloaded in repo_download folder
repo_link = str(input("Enter link of repository: "))            #Take repo link as input 
access_profile(repo_link)                                       #Send link for analysis
test_yara()