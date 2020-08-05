# Outputs dot graph of the phrase tree for the SWUM identifier with the given id

import sys
from lxml import etree
from graphviz import Digraph

tag_to_label = {'swum_phrase': 'SP', 'verb_phrase': 'VP', 'noun_phrase': 'NP', 'prepositional_phrase': 'PP', 'verb_group': 'VG', 'noun_phrase_equivalence': 'EQ_NP', 'verb_phrase_equivalence': 'EQ_VP', 'unknown_phrase': 'UP'}

def visualize_swum_phrase(swum_phrase: etree._Element):
    def _visualize_rec(element: etree._Element, node_label: str):
        # static counter to differentiate between graph nodes with same label
        if 'counter' not in _visualize_rec.__dict__:
            _visualize_rec.counter = 0

        for child in element:
            # handle nested swum_identifiers
            if child.tag == 'swum_identifier':
                child_swum_phrase = next(grand_child for grand_child in child if grand_child.tag == 'swum_phrase')

                child_node_label = 'swum_phrase{}'.format(_visualize_rec.counter)
                g.node(child_node_label, label=tag_to_label['swum_phrase'])

                swum_attr = child.get('swum_attr')
                if swum_attr is not None:
                    g.edge(node_label, child_node_label, label=swum_attr)
                else:
                    g.edge(node_label, child_node_label)
                
                _visualize_rec.counter += 1
                _visualize_rec(child_swum_phrase, child_node_label)
            # normal case
            else:
                child_node_label = '{}{}'.format(child.tag, _visualize_rec.counter)
                
                if child.tag in tag_to_label:
                    g.node(child_node_label, label=tag_to_label[child.tag])
                else:
                    g.node(child_node_label, label=child.text.lower(), xlabel=child.tag)

                swum_attr = child.get('swum_attr')
                if swum_attr is not None:    
                    g.edge(node_label, child_node_label, label=swum_attr)
                else:
                    g.edge(node_label, child_node_label)
                
                _visualize_rec.counter += 1
                _visualize_rec(child, child_node_label)

    g = Digraph('G')
    g.node('swum_phrase', label=tag_to_label['swum_phrase'])

    _visualize_rec(swum_phrase, 'swum_phrase')

    g.save(filename='swum_phrase.gv')


def main(argv):
    if len(argv) != 3:
        print('expected args: phrases_output_file id')
        sys.exit(1)
    
    filename = argv[1]
    swum_id = argv[2]

    with open(filename, 'rb') as input_f:
        for _, element in etree.iterparse(input_f, tag='swum_identifier'):
            swum_phrase = None
            cur_id = None
            for child in element:
                if child.tag == 'swum_phrase':
                    swum_phrase = child
                elif child.tag == 'id':
                    cur_id = child.text

            if swum_phrase is not None and cur_id is not None and cur_id == swum_id:
                visualize_swum_phrase(swum_phrase)
                sys.exit(0)
        
        print('Could not find swum identifier with id {} in {}'.format(swum_id, filename))

if __name__ == '__main__':
    main(sys.argv)
