import ConfigParser

Config = ConfigParser.ConfigParser()

Config.read("qlf.cfg")

sections = Config.sections()

dict = {}

for section in sections:
    options = Config.options(section)
    for option in options:
        try:
            dict[option] = Config.get(section, option)
            if dict[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict[option] = None

print dict
