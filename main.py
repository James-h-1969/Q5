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

A_STAR_B_STAR = {
    "V" :['S','X', 'Y', 'A', 'B'],
    "T" : ['a', 'b'],
    "start" : 'S',
    "rules" : [('S', ('X', 'Y')),
            ('S', ('A', 'X')),
            ('S', ('B', 'Y')),
            ('S', tuple()),
            ('S', ('a',)),
            ('S', ('b',)),
            ('X', ('A', 'X')),
            ('Y', ('B', 'Y')),
            ('X', ('a',)),
            ('Y', ('b',)),
            ('A', ('a',)),
            ('B', ('b',)),
            ]
}

A_N_B_N = {
    "V" :['S','X', 'T', 'B', 'A'],
    "T" : ['a', 'b'],
    "start" : 'S',
    "rules" : [('S', ('A', 'X')),
            ('S', tuple()),
            ('T', ('A','X')),
            ('X', ('T','B')),
            ('X', ('b', ) ),
            ('A', ('a', ) ),
            ('B', ('b', ) )
            ]
}


# S -> aSb | ε  ||| 
# S -> T, T -> aSb | e ||| 
# 


def get_new_cfg():
    # read a CFG via stdin. See parser.py for details on the returned object
    cfg = parse_cfg()
    # cfg= A_N_B_N
    rules_to_omit = []
    for rule in cfg["rules"]:
        left_side, right_side = rule
        if (len(right_side) == 1 and left_side == "S"):
            if right_side == ():
                pass
            else:
                rules_to_omit.append(rule)

    for rule in rules_to_omit:
        cfg["rules"].remove(rule)


    # construct a new CFG, then output it to stdout.
    # find a rule where A -> a, X -> a, Y -> a
    final_variable = []
    for rule in cfg["rules"]:
        left_side, right_side = rule 
        if len(right_side) == 1:
            # we need to check there are no other rules with that variable on the left
            counter = 0
            for new_rule in cfg["rules"]:
                left, right = new_rule
                if (left == left_side):
                    counter += 1
            if counter == 1:
                final_variable.append((left_side, right_side[0]))
            else:
                # remove the rule going to one thing
                for new_rule in cfg["rules"]:
                        left, right = new_rule
                        if (left == left_side):
                            if (len(right_side)) == 1:
                                index_of = cfg["rules"].index(rule)
                                cfg["rules"][index_of] = (0,0) #we want to ignore
        

    if final_variable == "":
        return cfg #if no rule then only accept 0 "a"'s -> SAME CFG as start
    
   
    # have a counter of the amount of A's
    no_a = [] # we accept
    one_a = []
    two_a = []
    three_a = []
    four_a = []
    single_rules = []

    new_Variables = []

    for variable,terminal in final_variable:
        new_Variables.append(variable)

    for rule in cfg["rules"]:
        left_side, right_side = rule 
        if left_side == 0 and right_side == 0:
            continue
        # if the right side
        if len(right_side) == 2: #this means it doesnt go to a terminal
            if left_side == "S":
                dup_range = 1
            else:
                dup_range = 5
            for i in range(dup_range): #we make five copies 
                index = i
                next_index = (index + 1) % 5
            
                if checkDerive(right_side[0], final_variable):
                    if (index == 0):
                        single_rules.append((left_side + str(index), tuple()))
                    new_rule = (left_side + str(index), (right_side[0], right_side[1] + str(next_index)))
                    new_Variables.append(left_side + str(index))
                    new_Variables.append(right_side[1] + str(next_index))
                elif checkDerive(right_side[1], final_variable):
                    if (index == 0):
                        single_rules.append((left_side + str(index), tuple()))
                    new_rule = (left_side + str(index), (right_side[0] + str(next_index), right_side[1]))
                    new_Variables.append(left_side + str(index))
                    new_Variables.append(right_side[0] + str(next_index))

                else:
                    if (right_side[0] in [x[0] for x in final_variable]):
                        new_rule = (left_side + str(index), (right_side[0], right_side[1] + str(index)))
                        new_Variables.append(right_side[0] + str(index))
                    elif (right_side[1] in [x[0] for x in final_variable]):
                        new_rule = (left_side + str(index), (right_side[0] + str(index) , right_side[1]))
                        new_Variables.append(right_side[1] + str(index))
                    new_Variables.append(left_side + str(index))                    

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
            if left_side in [x[0] for x in final_variable]:
                new_rule = (left_side, right_side)  
            else:
                new_rule = (left_side + str(0), right_side)
                new_Variables.append(left_side + str(0))
            single_rules.append(new_rule)

    new_Variables = list(set(new_Variables)) #removes duplicates 
    rules = list(set(no_a + one_a + two_a + three_a + four_a + single_rules))
    cfg["rules"] = rules
    cfg["V"] = new_Variables
    cfg["start"] = "S0"


    return cfg


def checkDerive(side, final_variable):
    for variable, terminal in final_variable:
        if side == variable and terminal == "a":
            return True
    return False
    


if __name__ == '__main__':
    cfg = get_new_cfg()
    # if you use the same data structure, you can use:
    print_cfg(cfg)
