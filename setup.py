import urllib.request
import zipfile, os
from time import sleep

def clear():

  # for windows
  if os.name == 'nt':
      _ = os.system('cls')

  # for mac and linux(here, os.name is 'posix')
  else:
      _ = os.system('clear')

if __name__ == "__main__":
  print("Installing requirements and venv")
  #make virtualenv .venv if not already exists and install requirements in .venv for windows and linux
  if not os.path.exists('.venv'):
    print("Creating virtualenv")
    if os.name == 'nt':
      os.system('python -m venv .venv')
      os.system('.venv\Scripts\pip install -r requirements.txt')
    else:
      os.system('python -m venv .venv')
      os.system('.venv/bin/pip install -r requirements.txt')
  else:
    print("Virtualenv already exists")
  sleep(2)
  clear()
  
  print("Checking for chromedriver")
  if os.name == 'nt':
    os.system('.venv\Scripts\python chromedriver.py')
  else:
    os.system('.venv/bin/python chromedriver.py')
  clear()

  #make directory ss if not already exists
  if not os.path.exists('ss'):
    print("Creating directory ss")
    os.makedirs('ss')
  else:
    print("Directory ss already exists")
  clear()

  #make directory ss if not already exists
  if not os.path.exists('error'):
    print("Creating directory error")
    os.makedirs('error')
  else:
    print("Directory error already exists")
  clear()

  #rename example_config.ini to config.ini
  if not os.path.exists('config.ini'):
    print("Renaming example_config.ini to config.ini")
    os.rename('example_config.ini', 'config.ini')
  else:
    print("config.ini already exists")
  clear()

  print("Now Fill up config.ini")
  sleep(5)



