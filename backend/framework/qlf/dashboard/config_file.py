import os

qlf_root = os.getenv('QLF_ROOT')
config_path = '{}/framework/config/qlf.cfg'.format(qlf_root)


def edit_qlf_config_file(key, value):
    with open(config_path, 'r') as file:
        config = file.readlines()

    for i, line in enumerate(config):
        if key in line:
            config[i] = '{}={}\n'.format(key, value)

    with open(config_path, 'w') as file:
        file.writelines(config)
