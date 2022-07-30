import os
import stat
import shutil

repo_path = "D:/FlipKart_GRID/H1N1/repo_download"

shutil.rmtree(repo_path)
#os.chmod(repo_path, stat.S_IWRITE)
#os.remove(repo_path)

from git.repo.base import Repo
Repo.clone_from("https://github.com/AceLewis/my_first_calculator.py", repo_path)

 