""" This module contains a very simple parser to help you read the input files.
You don't need to edit this file, but you can if you want. You can even delete
it, if you'd prefer to write your own parsing functions."""

from sys import stdin

EPSILON = {'Epsilon', 'epsilon', 'EPSILON', 'ϵ', 'ε'}

def next_line(stream):
    for line in stream:
        line = line.split(';')[0].strip()
        if not line:
            continue
        yield line

def parse_cfg(stream=stdin):
    """Read from the stream, return a dictionary representing the CFG.

    key 'V' gives the set of variable labels (as a list)
    key 'T' gives the set of terminals (as a list)
    key 'start' gives the label of the start variable
    key 'rules' gives a list of (V, production) tuples, representing rules V -> production
      productions are tuples of variables/terminals
      epsilon productions are empty tuples

    e.g. if the only rules were
        X -> a b | epsilon
        Foo -> b
    Then the dictionary entry for 'rules' would be:
        [('X', ('a', 'b')),
         ('X', tuple()),
         ('Foo', ('b',))
         ]

    This is not a very efficient representation of a CFG, feel free to 
    use this data to construct a data structure you prefer.
    """
    it = iter(next_line(stream))
    cfg = dict()
    cfg['V'] = next(it).split('=')[1].split()
    cfg['T'] = next(it).split('=')[1].split()
    cfg['start'] = next(it).split('=')[1].strip()
    # the remaining lines are the production rules
    cfg['rules'] = []
    for line in it:
        variable, productions = line.split('->')
        variable = variable.strip()
        for production in productions.split('|'):
            production = production.split()
            production = tuple(filter(lambda x: x not in EPSILON, production))
            cfg['rules'].append((variable, production))
    return cfg

def print_cfg(cfg):
    """Output a CFG to stdout"""
    output = []
    output.append(f"V = {' '.join(cfg['V'])}")
    output.append(f"Q = {' '.join(cfg['T'])}")
    output.append(f"start = {cfg['start']}")
    for variable, production in cfg['rules']:
        if production:
            output.append(f"{variable} -> {' '.join(production)}")
        else:
            output.append(f"{variable} -> epsilon")
    print('\n'.join(output))
