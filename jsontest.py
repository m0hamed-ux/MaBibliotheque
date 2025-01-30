import json

# Open and load JSON from a file
with open("Database/settings.json", "r") as file:
    data_dict = json.load(file)


print(data_dict)
print(data_dict["login"])
print(data_dict["password"])
