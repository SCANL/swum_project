import sys
import os
import subprocess

def run_layer(input_filename: str) -> (int, str):
    output_filename = 'temp_output.xml'
    command_str = '. ./swum_phrases {} {}'.format(input_filename, output_filename)
    completed_proc = subprocess.run(['/bin/bash', '-i', '-c', command_str])

    output_text = None
    if completed_proc.returncode == 0:
        with open(output_filename, 'r') as output_f:
            output_text = output_f.read().replace('\n', '')

        subprocess.run(['rm', output_filename])

    return completed_proc.returncode, output_text

def test_simple_success():
    ret, text = run_layer('tests/testcases/simple_success.xml')
    assert ret == 0

def test_missing_metadata():
    ret, text = run_layer('tests/testcases/missing_metadata.xml')
    assert ret != 0

def test_invalid_xml():
    ret, text = run_layer('tests/testcases/invalid.xml')
    assert ret != 0
