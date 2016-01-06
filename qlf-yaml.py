import pickle
import yaml

with open("testConfig1.yaml", 'r') as stream:
    testConfig = yaml.load(stream)

print testConfig 
