import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description='build a set of projects'
        )
    parser.add_argument(
        'command', help='The command to run')
    return parser.parse_args()
