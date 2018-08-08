import argparse
import os
import sys


def init_args(argv):
    parser = argparse.ArgumentParser(description='Checks files bitwise equality', prog='bwc.py')
    parser.add_argument('f1', nargs=1, help='first file to compare', metavar='<file1_path>')
    parser.add_argument('f2', nargs=1, help='second file to compare', metavar='<file2_path>')
    try:
        return parser.parse_args(argv)
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit(2)


def check_file(file):
    try:
        return os.stat(file)
    except FileNotFoundError:
        print("Can't read file ", file)
        sys.exit(2)


def main(argv):
    a = init_args(argv)
    s1 = check_file(a.f1[0])
    s2 = check_file(a.f2[0])

    if s1.st_size == s2.st_size:
        fr1 = open(a.f1[0], 'rb').read()
        fr2 = open(a.f2[0], 'rb').read()

        flag = True

        for i in range(fr1.__len__()):
            if fr1.__getitem__(i) != fr2.__getitem__(i):
                flag = False
                break

        if flag:
            print("Files are identical")
        else:
            print("Files are different")

    else:
        print("Different file lengths")


if __name__ == "__main__":
    main(sys.argv[1:])
