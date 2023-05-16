import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == '__main__':
    with open('requirements.txt', 'r') as f:
        for line in f.readlines():
            install(line.strip())
