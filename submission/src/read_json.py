import json

json_data = json.load(open("miserables.json"))
for i, node in enumerate(json_data["nodes"]):
    print(i, node)
for i, link in enumerate(json_data["links"]):
    print(i, link)
