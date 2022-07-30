import yara
import os
import collections

rules_path_dict = collections.defaultdict(str)
rules_path = "D:/FlipKart_GRID/H1N1/yara_rules"

i = 0
for r in os.listdir(rules_path):
    dir = os.path.join(rules_path, r)
    #print(dir)
    file_name, file_extension = os.path.splitext(dir)
    if(file_extension == ".yar"):
        print(dir)
        rules_path_dict[str(i)] = dir
        i += 1

rules = yara.compile(filepaths = rules_path_dict)
rules.save("D:/FlipKart_GRID/H1N1/compiled_yara_rules/final_compiled")
print("Rules compiled successfully!")


