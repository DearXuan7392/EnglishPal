'''
Yaml.py
配置文件包括:
    ./static/config.yml
    ./layout/partial/header.html
    ./layout/partial/footer.html
'''
import yaml as YAML
import os

path_prefix = './'  # comment this line in deployment

ymlPath = path_prefix + 'static/config.yml'
partialPath = path_prefix + 'layout/partial/'
f = open(ymlPath, 'r', encoding='utf-8')
cont = f.read()  # 以文本形式读取yaml

yml = YAML.load(cont, Loader=YAML.FullLoader)  # 加载yaml

with open(partialPath + 'header.html', 'r', encoding='utf-8') as f:
    yml['header'] = f.read()

with open(partialPath + 'footer.html', 'r', encoding='utf-8') as f:
    yml['footer'] = f.read()
