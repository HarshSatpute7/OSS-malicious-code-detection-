import yara
import os

valid_extensions = {'.c', '.cpp', '.py', '.java', '.m', '.html', '.css', '.js', '.sh', '.r', '.php', '.xhtml', '.net'} 
invalid_files = {".git", ".gitignore", ".gitattributes"} 

repo_path = "D:/FlipKart_GRID/H1N1/repo_download"
rules = yara.load("D:/FlipKart_GRID/H1N1/compiled_yara_rules/final_compiled") 

def check(repo_path):
    for f in os.listdir(repo_path):
        dir = os.path.join(repo_path, f)
        #print(dir)
        file_name, file_extension = os.path.splitext(dir)
        #print(f)
        #print(file_name)
        #print(file_extension)
        if(file_extension in valid_extensions):
            matches = rules.match(dir)
            print(f + " contains : ", end="")
            print(matches)
        if(not file_extension and f not in invalid_files):
            print("Its going inside the loop! YAAAY!")
            check(file_name)
        
        
check(repo_path)


