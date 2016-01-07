import yaml
import json

with open('test.json', 'r') as fp:
    data = json.load(fp)

with open('data.yaml', 'w') as fp2:
    yaml.safe_dump(data,fp2)

