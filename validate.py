import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
ICONS_DIR = os.path.join(os.path.dirname(__file__), 'icons')


def validate_entity(e):
  assert 'name' in e
  assert 'icon' in e
  assert os.path.exists(os.path.join(ICONS_DIR, e['icon']))
  assert e['icon'].endswith('.png')


def main():
  data = json.load(open(CONFIG_PATH))
  for k, v in data.items():
    if k == 'default':
      for e in v:
        validate_entity(e)
    else:
      validate_entity(v)


if __name__ == '__main__':
  main()
  