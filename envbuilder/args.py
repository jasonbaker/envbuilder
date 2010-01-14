import argparse

def get_arg_parser():
    parser = argparse.ArgumentParser(
        description='build a set of projects'
        )
    parser.add_argument('-p', '--parcels', default=None,
                        help='A comma-separated list of parcels to update.')
    return parser
