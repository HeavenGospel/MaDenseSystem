import os
import yaml


def load_config(config_file):
    with open(os.path.join(os.path.dirname(__file__), config_file + '.yaml'), 'r', encoding='utf-8') as file:  # 指定编码为 utf-8
        config = yaml.safe_load(file)
    return config