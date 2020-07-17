import sys
import os
import subprocess

def run_layer(input_filename: str) -> (int, str):
    output_filename = 'temp_output.xml'
    command_str = '. ./swum_phrases {} {}'.format(input_filename, output_filename)
    completed_proc = subprocess.run(['/bin/bash', '-i', '-c', command_str])

    output_f = open(output_filename, 'r')
    output_text = output_f.read()
    output_f.close()

    subprocess.run(['rm', output_filename])

    return completed_proc.returncode, output_text.replace('\n', '')

def test_simple_success():
    ret, text = run_layer('tests/simple_success.xml')
    assert ret == 0
    assert text == '<prepositional_phrase><preposition>My</preposition><noun_phrase><noun>Class</noun></noun_phrase></prepositional_phrase><verb_phrase><action><verb_group><verb>get</verb></verb_group></action><theme><noun_phrase><noun>Area</noun></noun_phrase></theme><aux_arg><noun_phrase><noun>x</noun></noun_phrase></aux_arg><aux_arg><noun_phrase><noun>y</noun></noun_phrase></aux_arg><aux_arg><noun_phrase><noun>int</noun></noun_phrase></aux_arg><aux_arg><prepositional_phrase><preposition>My</preposition><noun_phrase><noun>Class</noun></noun_phrase></prepositional_phrase></aux_arg></verb_phrase>'

def test_missing_metadata():
    ret, text = run_layer('tests/missing_metadata.xml')
    assert ret != 0

def test_invalid_xml():
    ret, text = run_layer('tests/invalid_xml.xml')
    assert ret != 0
