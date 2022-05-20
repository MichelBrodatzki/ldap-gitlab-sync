import argparse

def add_referat(filename, referat):
    pass

def remove_referat(filename, referat):
    pass

def main():
    parser = argparse.ArgumentParser(description="Manages a list, which maps FS-ETEC Referate to GitLab groups")
    parser.add_argument('filename', type=str, help='Path to mapping file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add', type=str, metavar="REFERAT", help="Adds FS-ETEC Referat")
    group.add_argument('--remove', type=str, metavar="REFERAT", help="Removes FS-ETEC Referat")
    args = parser.parse_args()

    if args.add:
        add_referat(args.filename, args.add)

    if args.remove:
        remove_referat(args.filename, args.remove)
