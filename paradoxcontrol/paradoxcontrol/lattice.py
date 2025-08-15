from enum import Enum

class TV(str, Enum):
    T = "T"   # true
    F = "F"   # false
    B = "B"   # both (localized contradiction)
    N = "N"   # neither/unknown

def tv_neg(x: TV) -> TV:
    return {"T":"F","F":"T","B":"B","N":"N"}[x]

def tv_join(a: TV, b: TV) -> TV:  # OR (info order)
    if a == b: return a
    if "B" in (a, b): return TV.B
    if (a, b) in [(TV.T, TV.F), (TV.F, TV.T)]: return TV.B
    if (a, b) in [(TV.T, TV.N), (TV.N, TV.T)]: return TV.T
    if (a, b) in [(TV.F, TV.N), (TV.N, TV.F)]: return TV.F
    return TV.B

def tv_meet(a: TV, b: TV) -> TV:  # AND (conservative)
    if a == b: return a
    if TV.N in (a, b): return TV.N
    if (a, b) in [(TV.T, TV.F), (TV.F, TV.T)]: return TV.N
    if (a == TV.B and b == TV.T) or (a == TV.T and b == TV.B): return TV.T
    if (a == TV.B and b == TV.F) or (a == TV.F and b == TV.B): return TV.F
    if a == TV.B and b == TV.B: return TV.B
    return TV.N

def tv_from_sc(support: float, counter: float, eps: float=1e-9) -> TV:
    s = support > eps; c = counter > eps
    if s and not c: return TV.T
    if c and not s: return TV.F
    if s and c:     return TV.B
    return TV.N
