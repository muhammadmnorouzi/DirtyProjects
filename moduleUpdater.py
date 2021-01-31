import os


os.system("pip freeze >> rq.txt")

#open rq.txt
with open("rq.txt") as file:
    data = file.read()

data = data.split()

new_data = []
#delete == and version
for mo in data:
    p = mo.find("=")
    new_data.append(mo[:p])

#upgrade all modules
for item in new_data:
    os.system("pip install --upgrade " + item)

