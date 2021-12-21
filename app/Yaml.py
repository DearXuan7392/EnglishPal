import yaml as YAML
import os


path_prefix = './'  # comment this line in deployment


filepath = path_prefix + 'static/config.yml'
f = open(filepath, 'r', encoding='utf-8')
cont = f.read()

yml = YAML.load(cont, Loader=YAML.FullLoader)