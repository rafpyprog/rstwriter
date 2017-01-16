import os
import sys

SETUP_FILE = 'setup.py'

if sys.argv is None:
    print('Version number argument missin.')
    sys.exit()

# cria nova tag no github e faz o push.
version = sys.argv[1]
os.system('git tag {} -m "Version {} tag"'.format(version, version))
os.system('git push --tags origin master')

# atualiza o arquivo de setup
with open(SETUP_FILE, 'r') as setup:
    lines = setup.readlines()

newsetup = []
for line in lines:
    # atualiza a versão do pacote
    if 'version' in line:
        newsetup.append(line.split('=')[0] + '=' + "'{}',\n".format(version))
    # atualiza o endereço do arquivo tar do github
    elif line.strip(' ').startswith('download_url'):
        config = line.split('=')
        url = config[1].split('/')
        url[-1] = "{}',\n".format(version)
        print(url)
        newurl = "https://" + "/".join(url[2:])
        print(newurl)
        newsetup.append(line.split('=')[0] + "=" + "'" + newurl)
    else:
        newsetup.append(line)

with open(SETUP_FILE, 'w') as newsetupfile:
    for line in newsetup:
        newsetupfile.write(line)
