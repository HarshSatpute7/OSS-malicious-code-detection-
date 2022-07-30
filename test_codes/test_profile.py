import requests

# Create an API request 
url = "https://api.github.com/search/repositories?q=stamparm/maltrail" 
response = requests.get(url)
print("Status code: ", response.status_code)
# In a variable, save the API response.
response_dict = response.json()
# Evaluate the results.
print(response_dict.keys())

print("Total repos:", response_dict['total_count'])
# find total number of repositories
repos_dicts = response_dict['items']
print("Repos found:", len(repos_dicts))
# examine the first repository
repo_dict = repos_dicts[0]
print("Keys:", len(repo_dict))
for key in sorted(repo_dict.keys()):
 print(key)

repos_dicts = response_dict['items']
print("Repositories found:", len(repos_dicts))
# Examine the first repository.
repo_dict = repos_dicts[0]
print("\nThe following is some information regarding the first repository:")
print('Name:', repo_dict['name'])  #print the project's name
print('Owner:', repo_dict['owner']['login'])  #use the key owner and the the key login to get the dictionary describing the owner and the owner’s login name respectively.
print('Stars:', repo_dict['stargazers_count'])  #print how many stars the project has earned
print('Repository:', repo_dict['html_url'])  #print URL for the project’s GitHub repoitory
print('Created:', repo_dict['created_at'])  #print when it was created
print('Updated:', repo_dict['updated_at'])  #show when it was last updated
print('Description:', repo_dict['description']) #print the repository’s description