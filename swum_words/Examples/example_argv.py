import sys

def main(argv):
    sys.argv[0]
    for index, arg in enumerate(argv):
        print('argument {}: {}'.format(index))

if __name__ == '__main__':
    main(sys.argv)
