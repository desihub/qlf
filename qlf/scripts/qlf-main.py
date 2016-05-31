import ConfigParser
import os

Config = ConfigParser.ConfigParser()

Config.read("config/qlf.cfg")

sections = Config.sections()

dic = {}

for section in sections:
    options = Config.options(section)
    for option in options:
        try:
            dic[option] = Config.get(section, option)
            if dic[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dic[option] = None

print "Config file contents: ", dic

if Config.has_option("namespace","datadir"):
    path = Config.get("namespace","datadir")

fullpath = os.path.join(path,"config")

print "The full path to the config folder is: ", fullpath
