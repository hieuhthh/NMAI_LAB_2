import os
import shutil
from copy import deepcopy

STR_SPLIT = ' OR '
NEG_SYMBOL = '-'
NEG_POS = len(NEG_SYMBOL)

def str2clause(str):
    return str.split(STR_SPLIT)

def clause2str(clause):
    return STR_SPLIT.join(clause)

def clean_clause(clause):
    """
    ['-B', 'A', '-B', '-A', 'C', 'B']
    ->
    ['A', '-A', 'B', '-B', 'C']
    """
    def compare(lit):
        if is_neg(lit):
            return abs(lit) + '1'
        else:
            return abs(lit) + '0'
    return sorted(list(set(clause)), key=compare)

def clean_clauses(clauses):
    cleans = [clean_clause(clause) for clause in clauses]
    return sorted(cleans)

def read_file(filepath):
    clauses = []

    with open(filepath, "r") as f:
        data = f.read().splitlines()
        while data[-1] == '':
            del data[-1]

        alpha = data[0].split(STR_SPLIT)
        alpha = clean_clause(alpha)

        for i in range(int(data[1])):
            line = data[2 + i]
            clause = str2clause(line)
            clauses.append(clause)

        clauses = clean_clauses(clauses)

    return alpha, clauses

def is_neg(lit):
    if lit[0] == NEG_SYMBOL:
        return True
    return False

def abs(lit):
    if is_neg(lit):
        return lit[NEG_POS:]
    return lit

def neg_lit(lit):
    """
    negative of 1 literal
    """
    if is_neg(lit):
        return abs(lit)
    return NEG_SYMBOL + lit

def neg_clause(clause):
    """
    clause: list of literal
    """
    ans = []
    for lit in clause:
        ans.append(neg_lit(lit))
    return ans

def add_alpha(clauses, alpha):
    neg_alpha = neg_clause(alpha)
    for lit in neg_alpha:
        clauses.append([lit])
    return clauses

def complent(lit1, lit2):
    if abs(lit1) == abs(lit2) and is_neg(lit1) != is_neg(lit2):
        return True
    return False

def is_true(clause):
    for i in range(len(clause)):
        for j in range(i + 1, len(clause)):
            if complent(clause[i], clause[j]):
                return True
    return False

def pl_resolve(clause1, clause2):
    clauses = []

    for i in range(len(clause1)):
        for j in range(len(clause2)):
            if complent(clause1[i], clause2[j]):
                cp_clause1 = deepcopy(clause1)
                cp_neg_clause2 = deepcopy(clause2)
                del cp_clause1[i]
                del cp_neg_clause2[j]

                clause = cp_clause1 + cp_neg_clause2
                clause = clean_clause(clause)
                clauses.append(clause)

    return clauses

def pl_resolution(alpha, clauses, debug=False):
    alpha = deepcopy(alpha)
    clauses = deepcopy(clauses)

    clauses = add_alpha(clauses, alpha)
    clauses = clean_clauses(clauses)

    step_clauses = []

    while True:
        new_clauses = []

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvents = pl_resolve(clauses[i], clauses[j])

                for resolvent in resolvents:
                    if is_true(resolvent):
                        continue

                    if resolvent not in clauses and resolvent not in new_clauses:
                        new_clauses.append(clean_clause(resolvent))
                        if debug:
                            print(resolvent, "from:", clause2str(clauses[i]), "with", clause2str(clauses[j]))

        step_clauses.append(new_clauses)
        clauses = clauses + new_clauses

        if len(new_clauses) == 0:
            return False, step_clauses

        if [] in new_clauses:
            return True, step_clauses

        if debug:
            print('-'*10)

def write_txt(filepath, solve, step_clauses):
    with open(filepath, "w") as f:
        for step in step_clauses:
            f.write(str(len(step)) + '\n')
            step = sorted(step)
            if len(step) >= 1 and step[0] == []:
                step.append([])
                del step[0]
            for clause in step:
                if clause == []:
                    f.write('{}\n')
                else:
                    f.write(clause2str(clause) + '\n')

        if solve:
            f.write('YES')
        else:
            f.write('NO')

def solve_end2end(input_path, output_path, debug=False):
    try:
        alpha, clauses = read_file(input_path)
        solve, step_clauses = pl_resolution(alpha, clauses, debug)
        print('YES' if solve else 'NO')
        write_txt(output_path, solve, step_clauses)
    except Exception as error:
        print('*'*10, 'Found ERROR', '*'*10)
        print(error)
        raise

def make_dir(dir):
    try:
        shutil.rmtree(dir)
    except:
        pass

    try:
        os.mkdir(dir)
    except:
        pass
    

