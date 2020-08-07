"""Implementation of SWUM bridges layer"""

import sys
from lxml import etree

supported_constructs = ['function', 'class', 'constructor', 'interface']

def main(argv):
    if len(argv) != 3:
        print('expected args: srcml_file id')
        sys.exit(1)
    
    filename = argv[1]
    swum_id = argv[2]

    with open(filename, 'rb') as input_f:
        for event, element in etree.iterparse(input_f, events=('start', 'end')):
            if event == 'end':
                element.clear(keep_tail=True)
                continue

            # skip elements that are either missing a swum_id or have a swum_id that differs from what the user is searching for
            element_id = element.get('swum_id')
            if element_id is None or element_id != swum_id:
                continue

            tag = element.tag

            # remove xml namespace from tag name, if necessary
            try:
                last_brace = tag.index('}')
                tag = tag[last_brace+1:]
            except ValueError:
                pass

            if tag in supported_constructs:
                print(etree.tostring(element, encoding='utf-8', pretty_print=True).decode('utf-8'))
                sys.exit(0)
            else:
                print('{} is not a supported construct for the SWUM bridge layer'.format(tag))
                print('The following constructs are currently supported: {}'.format(', '.join(supported_constructs)))
                sys.exit(1)

        print('Could not find a supported swum_identifier with id {}'.format(swum_id))
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
