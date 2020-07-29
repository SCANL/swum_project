import sys
from lxml import etree
from graphviz import Digraph

# TODO: make the lexical tokens use full name adjacent to graph node (mimicking style of paper)
# tag_to_label = {'swum_phrase': 'SP', 'verb_phrase': 'VP', 'noun_phrase': 'NP', 'prepositional_phrase': 'PP', 'verb_group': 'VG', 'noun': 'N', 'noun_modifier': 'NM', 'preposition': 'P', 'verb_modifier': 'VM', 'verb': 'V', 'verb_particle': 'VPR'}
tag_to_label = {'swum_phrase': 'SP', 'verb_phrase': 'VP', 'noun_phrase': 'NP', 'prepositional_phrase': 'PP', 'verb_group': 'VG'}

def visualize_swum_phrase(swum_phrase: etree._Element):
    def _visualize_rec(element: etree._Element, node_label: str):
        if 'counter' not in _visualize_rec.__dict__:
            _visualize_rec.counter = 0

        for child in element:
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

    g = Digraph('G', filename='swum_phrase.gv')
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
                else:
                    print('skipping {}'.format(child.tag))

            if swum_phrase is not None and cur_id is not None and cur_id == swum_id:
                print(etree.tostring(element, encoding='utf-8', pretty_print=True).decode('utf-8'))
                visualize_swum_phrase(swum_phrase)
            else:
                print('skipping swum_phrase with id {}'.format(cur_id))

if __name__ == '__main__':
    main(sys.argv)