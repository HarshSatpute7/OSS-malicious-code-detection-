import yara
import os

rules_path = "D:/FlipKart_GRID/H1N1/yara_rules"

i = 0
for r in os.listdir(rules_path):
    dir = os.path.join(rules_path, r)
    #print(dir)
    file_name, file_extension = os.path.splitext(dir)
    if(file_extension == ".yar"):
        print(dir)
        rules = yara.compile(dir)
        #print(type(rules))
        rules.save("D:/FlipKart_GRID/H1N1/compiled_yara_rules/" + str(i))
        i += 1
print("Rules compiled successfully!")

