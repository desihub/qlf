import json
import yaml

with open('config/ql.json', 'r') as fp:
    data = json.load(fp)

root = {"PipeLine":[]}

for item in data["tasks"]:
    steps = []
    for item2 in item["steps"]:
        step = {}
        step["ModuleName"] = item2["source"]
        step["Name"] = item2["name"]
        config = {} 
        for item3 in item2["configuration"]:
            config[item3["label"]] = item3["default"]
        step["kwargs"] = config
        steps.append(step)
    root["PipeLine"].append({"StepName":item["name"],"Steps":steps})

print root
with open("config/ql.yaml","w") as fp:
    yaml.safe_dump(root,fp)
