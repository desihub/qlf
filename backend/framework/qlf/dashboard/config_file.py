import os
import shutil

qlf_root = os.getenv('QLF_ROOT')
config_path = '{}/framework/config/qlf.cfg'.format(qlf_root)


def edit_qlf_config_file(keys, values):
    with open(config_path, 'r') as file:
        config = file.readlines()

    for i, line in enumerate(config):
        for j, key in enumerate(keys):
            if key in line:
                config[i] = '{}={}\n'.format(keys[j], values[j])

    with open(config_path, 'w') as file:
        file.writelines(config)


def set_default_configuration():
    sfile = os.environ.get(
        'DEFAULT_QLF_CFG',
        '/app/framework/config/qlf.cfg.template'
    )
    dfile = os.environ.get('QLF_CFG', '/app/framework/config/qlf.cfg')
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)
