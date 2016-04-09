import config;
import math;

from math import log,factorial;
from error import Error;
from graph import Graph;
from model import Model;

### basic functions
# determine possible number of edges between `numEdges' nodes
def CalcCliqueNumPosEdges(numEdges):
  # directed graph, no self-loops
  # (|n|^2)-n
  return numEdges*numEdges - numEdges;

# (n choose k)
def choose(n, k):
 if 0 <= k <= n:
   p = 1
   for t in xrange(min(k, n - k)):
     p = (p * (n - t)) // (t + 1)
   return p;
 else:
   return 0;

def composition(n,k) :
    return choose(n-1,k-1);

def LC(n,k) :
    return log(composition(n,k),2);

def weakcomposition(n,k) :
    return choose(n+k-1,k-1);
    
def LwC(n,k) :
    return log(weakcomposition(n,k),2);

# Encoded length of `n` 0/1 entries with `k` 1s (aka, Naive Uniform)
def LnU(n,k):
    #print 'LnU', n, k
    if n==0 or k==0 or k==n or k > n:# added case k > n to solve overlap edge issues
        return 0;    
    x = -log(k / float(n),2);
    y = -log((n-k)/float(n),2);
    return k * x + (n-k) * y;
    
# Encoded length of `n` 0/1 entries with `k` 1s (aka, Uniform)
def LU(n,k) :
    if n==0 or k==0 :
        return 0;   
    return log(choose(n,k),2);

# encoded size of an integer >=1 as by Rissanen's 1983 Universal code for integers
def LN(z) :
  if z <= 0 :
    return 0;
  c = log(2.865064,2);
  i = log(z,2);
  while i > 0 :
    c = c + i;
    i = log(i,2);
  return c;

# find precision and scale of a number
def precision_and_scale(x):
    max_digits = 14;
    int_part = int(abs(x));
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1;
    if magnitude >= max_digits:
        return (magnitude, 0);
    frac_part = abs(x) - int_part;
    multiplier = 10 ** (max_digits - magnitude);
    frac_digits = multiplier + int(multiplier * frac_part + 0.5);
    while frac_digits % 10 == 0:
        frac_digits /= 10;
    scale = int(math.log10(frac_digits));
    return (magnitude + scale, scale);

# encoded size of a truncated real-valued parameter by Rissanen's 1983 Universal code
def LR(z) :
    (precision, scale) = precision_and_scale(z);
    z1 = math.modf(z);
    z2 = z - z1;
    z2 = z2 * (10 ** scale);
    #print z;
    c = 1;
    c += LN(scale);
    c += LN(z1);
    c += LN(z2);
    return c; 
