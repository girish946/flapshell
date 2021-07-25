import argparse
from flapshell.main import read_code, parse_c

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='C code parser written in python')
    parser.add_argument('files', metavar='F', type=str, nargs='+',
                        help='Input File')

    args = parser.parse_args()
    # print(args.files)
    code = read_code(args.files[0])
    parse_c(code)
