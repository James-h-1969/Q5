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
    "V" :['S', 'A', 'B'],
    "T" : ['a', 'b'],
    "start" : 'S',
    "rules" : [('S', ('A', 'B')),
               ('S', ('a', ) ),
               ('S', ('b', ) ),
                ('S', tuple()),
                ('S', ('A','A')),
                ('S', ('A','B')),
                ('S', ('B','B')),
                ('A', ('A','A')),
                ('B', ('B','B')),
                ('A', ('a', ) ),
                ('B', ('b', ) )
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


def get_new_cfg():
    # read a CFG via stdin. See parser.py for details on the returned object
    # cfg = parse_cfg()
    cfg= A_N_B_N
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
            final_variable.append((left_side, right_side[0])) 

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
            if left_side == right_side[0] or left_side == right_side[1]:
                #case of recursion
                if left_side == right_side[0] and left_side == right_side[1]: #case where they are all the same
                    if checkDeriveToTerminalA(right_side[0], final_variable): #derives to an A
                        for i in range(5):
                            next_i = (i + 1) % 5
                            new_rule = (right_side[0] + str(i), (right_side[0], right_side[0] + str(next_i)))
                            single_rules.append(new_rule)
                            new_Variables.append(right_side[0] + str(i))
                        single_rules.append((right_side[0] + "0", tuple()))
                        new_Variables.append(right_side[0] + "0")
                    else: #does not derive  to A, eg. B -> BB
                        single_rules.append((left_side + "1", right_side))

            elif left_side == "S":
                i = 0
                # CASES: - one A, two A, one B, two B
                
                ## CASE OF TWO AS ##
                two_as = isTwoAs(cfg["rules"], final_variable)
                if (checkDeriveToTerminalA(right_side[0], final_variable) and checkDeriveToTerminalA(right_side[1], final_variable)):
                    single_rules.append(("S0", (right_side[0], right_side[1] + "1")))
                
                ## CASES OF ONE AS  ##
                elif (checkDeriveToTerminalA(right_side[0], final_variable)):
                    if two_as:
                        extra = "0"
                    else:
                        extra = ""
                    if (checkDeriveToTerminal(right_side[1], final_variable)):
                        single_rules.append(("S0", (right_side[0]+extra, right_side[1]+"1")))
                    else:
                        single_rules.append(("S0", (right_side[0]+extra, right_side[1] + "1")))
                elif (checkDeriveToTerminalA(right_side[1], final_variable)):
                    if (checkDeriveToTerminal(right_side[0], final_variable)):
                        single_rules.append(("S0", (right_side[0]+"1", right_side[1]+extra)))
                    else:
                        single_rules.append(("S0", (right_side[0]+"1", right_side[1]+extra)))

                ## CASES OF TWO BS ##
                elif (checkDeriveToTerminal(right_side[0], final_variable) and checkDeriveToTerminal(right_side[1], final_variable)): #boths Bs
                        single_rules.append(("S0", (right_side[0], right_side[1] + "1")))
                
                ## case of ONE BS
                elif (checkDeriveToTerminal(right_side[0], final_variable)): #one B
                        single_rules.append(("S0", (right_side[0], right_side[1] + "0")))
                elif (checkDeriveToTerminal(right_side[1], final_variable)): #one B
                        single_rules.append(("S0", (right_side[0] + "0", right_side[1])))

                else:
                    single_rules.append(("S0", (right_side[0] + "0", right_side[1] + "0")))

                    
                
            
            else:
                for i in range(5): #we make five copies 
                    index = i
                    next_index = (index + 1) % 5
                    if checkDeriveToTerminalA(right_side[0], final_variable): #check if there is an "a" in the right side
                        if (index == 0):
                            single_rules.append((left_side + str(index), tuple()))
                        new_rule = (left_side + str(index), (right_side[0], right_side[1] + str(next_index)))
                        new_Variables.append(left_side + str(index))
                        new_Variables.append(right_side[1] + str(next_index))
                    elif checkDeriveToTerminalA(right_side[1], final_variable): #check if there is an "a" in the right side
                        if (index == 0):
                            single_rules.append((left_side + str(index), tuple()))
                        new_rule = (left_side + str(index), (right_side[0] + str(next_index), right_side[1]))
                        new_Variables.append(left_side + str(index))
                        new_Variables.append(right_side[0] + str(next_index))

                    else:
                        if (right_side[0] in [x[0] for x in final_variable]): #if a B is in right side
                            new_rule = (left_side + str(index), (right_side[0], right_side[1] + str(index)))
                        elif (right_side[1] in [x[0] for x in final_variable]): 
                            new_rule = (left_side + str(index), (right_side[0] + str(index) , right_side[1]))
                        else: 
                            new_rule = (left_side + str(index), (right_side[0] + str(index), right_side[1] + str(index)))                    

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


    new_Variables = sorted(list(set(new_Variables)), key=lambda x: x[0][0]) #removes duplicates 
    rules = sorted(list(set(no_a + one_a + two_a + three_a + four_a + single_rules)), key=lambda x: x[0][0])
    cfg["rules"] = rules
    cfg["V"] = new_Variables
    cfg["start"] = "S0"


    return cfg

def isTwoAs(rules, final_variables):
    variable_A = ""
    for variable, terminal in final_variables:
        if terminal == "a":
            variable_A = variable
    return ((variable_A, (variable_A, variable_A)) in rules)
        


def checkDeriveToTerminalA(side, final_variable):
    for variable, terminal in final_variable:
        if side == variable and terminal == "a":
            return True
    return False

def checkDeriveToTerminal(side, final_variable):
    for variable, terminal in final_variable:
        if side == variable:
            return True
    return False
    


if __name__ == '__main__':
    cfg = get_new_cfg()
    # if you use the same data structure, you can use:
    print_cfg(cfg)
