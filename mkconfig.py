import yaml
import json

with open('config/ql.json', 'r') as fp:
    data = json.load(fp)

with open('config/ql.yaml', 'w') as fp2:
    yaml.safe_dump(data,fp2)

