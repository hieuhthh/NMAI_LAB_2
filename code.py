import pickle, gzip, os, random
import sys
import os
import collections

from logic import *
from typing import Tuple, List

A = Atom('A')

B = Atom('B')

C = Atom('C')

Alpha = Not(A)

Form1 = OrList([Not(A), B])
Form2 = OrList([B, Not(C)])
Form3 = OrList([A, Not(B), C])
Form4 = OrList([Not(B)])

KB = createResolutionKB(verbose=5)

KB.tell(Form1)
KB.tell(Form2)
KB.tell(Form3)
KB.tell(Form4)

print(KB.ask(Alpha))