from parseCNF import parse_cfg, print_cfg

"""
key 'V' gives the set of variable labels (as a list)
    key 'T' gives the set of terminals (as a list)
    key 'start' gives the label of the start variable
    key 'rules' gives a list of (V, production) tuples, representing rules V -> production
      productions are tuples of variables/terminals
      epsilon productions are empty tuples

"""

# RULE : [('X', (A, B)), etc]

# CNFS:
"""
S -> TA 
T -> AA 
A -> a
"""

def get_new_cfg():
    # read a CFG via stdin. See parser.py for details on the returned object
    cfg = parse_cfg()
    # construct a new CFG, then output it to stdout.
    # find a rule where A -> a, X -> a, Y -> a
    final_variable = []
    for rule in cfg["rules"]:
        left_side, right_side = rule 
        if "a" in right_side:
            final_variable.append(left_side)
    if final_variable == "":
        return cfg #if no rule then only accept 0 "a"'s -> SAME CFG as start
    
    # have a counter of the amount of A's
    no_a = [] # we accept
    one_a = []
    two_a = []
    three_a = []
    four_a = []


    new_Variables = []

    for variable in final_variable:
        new_Variables.append(variable)

    for rule in cfg["rules"]:
        left_side, right_side = rule 
        # if the right side 
        if len(right_side) == 2: #this means it doesnt go to a terminal
            for i in range(5): #we make five copies
                index = i
                next_index = (index + 1) % 5
                if right_side[0] in final_variable:
                    new_rule = (left_side + str(index), (right_side[0], right_side[1] + str(next_index)))
                    new_Variables.append(left_side + str(index))
                    new_Variables.append(right_side[1] + str(next_index))
                elif right_side[1] in final_variable:
                    new_rule = (left_side + str(index), (right_side[0] + str(next_index), right_side[1]))
                    new_Variables.append(left_side + str(index))
                    new_Variables.append(right_side[0] + str(next_index))
                else:
                    # theres no Variable which derives to a
                    new_rule = (left_side + str(index), (right_side[0] + str(index) , right_side[1] + str(next_index)))
                    new_Variables.append(left_side + str(index))
                    new_Variables.append(right_side[1] + str(next_index))
                    new_Variables.append(right_side[0] + str(index))
                if i == 0:
                    no_a.append(new_rule)
                if i == 1:
                    one_a.append(new_rule)
                if i == 2:
                    two_a.append(new_rule)
                if i == 3:
                    three_a.append(new_rule)
                if i == 4:
                    four_a.append(new_rule)
        else:
            new_rule = (left_side + str(0), right_side[0])  

    
    cfg["rules"] = no_a + one_a + two_a + three_a + four_a
    cfg["V"] = new_Variables
    cfg["start"] = "S0"

    return cfg


    


if __name__ == '__main__':
    cfg = get_new_cfg()
    # if you use the same data structure, you can use:
    print_cfg(cfg)
