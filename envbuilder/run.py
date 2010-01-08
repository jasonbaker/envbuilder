import os.path

from envbuilder.config import Config
from envbuilder.checkout import Checkout

commands = { 'checkout' : Checkout,
             'co' : Checkout,
             }

def main():
    cwd = os.path.abspath(os.path.curdir)
    filepath = os.path.join(cwd, '.env')
    config = Config(filepath)
    sections = config.project.repos
    
    
