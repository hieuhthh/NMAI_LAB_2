from copy import deepcopy

STR_SPLIT = ' OR '
NEG_SYMBOL = '-'
NEG_POS = len(NEG_SYMBOL)

def str2clause(str):
    return str.split(STR_SPLIT)

def clause2str(clause):
    return STR_SPLIT.join(clause)

def clean_clause(clause):
    return sorted(list(set(clause)), key=abs)

def clean_clauses(clauses):
    return [clean_clause(clause) for clause in clauses]

def read_file(filepath):
    clauses = []

    with open(filepath, "r") as f:
        data = f.read().splitlines()
        while data[-1] == '':
            del data[-1]

        alpha = data[0].split(STR_SPLIT)

        for i in range(int(data[1])):
            line = data[2 + i]
            clause = str2clause(line)
            clauses.append(clause)

        clauses = clean_clauses(clauses)

    return alpha, clauses

def add_alpha(clauses, alpha):
    neg_alpha = neg_clause(alpha)
    for lit in neg_alpha:
        clauses.append([lit])
    return clauses

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

filepath = 'input/input.txt'
alpha, clauses = read_file(filepath)

print(alpha)
print(clauses)

def resolve(clause1, clause2):
    clauses = []
    neg_clause2 = neg_clause(clause2)

    for i in range(len(clause1)):
        for j in range(len(neg_clause2)):
            if clause1[i] == neg_clause2[j]:
                cp_clause1 = deepcopy(clause1)
                cp_neg_clause2 = deepcopy(neg_clause2)
                del cp_clause1[i]
                del cp_neg_clause2[j]

                clause = cp_clause1 + cp_neg_clause2
                clause = clean_clause(clause)
                clauses.append(clause)

    return clauses

print(resolve(clauses[0], clauses[2]))
