
from discrete_variable import DiscreteVariable
from random_variable import RandomVariable as RV
from naturals import Naturals as N
import matplotlib.pyplot as plt
from scipy.special import comb
from reals import Reals as R
import numpy as np
import bernoulli 
import math


class Binomial(DiscreteVariable):

    def __init__(self, n: int=0, p: float=0):
        # Call super class with list of specifications
        super().__init__()
        # p need to be in (0,1) and n must be natural value
        assert p in R(0,1) and n in N(0,...,np.Inf)
        # Probability parameter p of success of bernoulli event
        self.p = p 
        # Number of independents events
        self.n = n

    def pmf(self, x: int) -> int:
        # P(X = k) = (n,k) * p^k * (1-p)^(n-k)
        return (comb(self.n, x) * (self.p ** x) * ((1 - self.p) ** (self.n - x))) * RV.I(x in N(0,...,self.n))

    def cdf(self, x: (float, int)) -> int:
        # P(X <= K) = ∑ P(X=k), k ∈ [1,n]
        return sum([self.pmf(k) for k in range(math.floor(x) + 1)]) + RV.I(x > self.n)

    def ev(self) -> float:
        # E(X) = ∑ (k * P(X=k)), k ∈ [1,n] = np
        return self.n * self.p 

    def var(self) -> float:
        # Var(X) = E(X^2) - E(X)^2 = np(1-p)
        return (self.n * self.p) * (1 - self.p)

    def devstd(self) -> float:
        # DevStd(X) = Var(X)
        return self.var() ** 0.5

    def fpmf(self, x: int, P: float) -> 'Binomial':
        # n need to be defined
        assert self.n is not None, Exception
        # Verify integrity of parameters
        assert x in N(0,...,np.Inf) and p in R(0,1)
        # The equation to which to apply the zero theorem
        f = lambda c: (comb(self.n,x) * c**x * (1-c)**(self.n-x)) - P
        # Given pmf(x) = P, return Binomial with parameter n and p
        return Binomial(self.n, R.bfzero(f, (0,1)))
        
    def fev(self, e: float) -> 'Binomial':
        # Almost one parameter need to be defined
        assert self.n is not None or self.p is not None, Exception
        # Expected value need to be in (0,1)
        assert e in R(0,1), Exception
        # if p is not defined
        if self.p is None: 
            # Given E(X) and n, return new Binomial with parameter p
            return Binomial(self.n, e/self.n) 
        # Given E(X) and p, return new Binomial with parameter n
        return Binomial(e/self.p, self.p)
        
    def fvar(self, v: float) -> 'Binomial':
        # Almost one parameter need to be specified
        assert self.n is not None or self.p is not None, Exception
        # Variance need to be in (0,1)
        assert v in R(0,1), Exception
        # if p is not defined
        if self.p is None: 
            # Given Var(X) and n, return Binomial with parameter p
            return Binomial(self.n, (1 + (1-(4*(v/self.n)))**0.5) / 2)
        # Given Var(X) and p, return Binomial with parameter n
        return Binomial(v/(self.p*(1-self.p)), self.p)
        
    def fdevstd(self, d: float):
        # Verify integrity of value d passed
        assert d in R(0,1), Exception
        # Given DevStd(X), return new Binomial with parameter p or n
        return self.fvar(d**2)

    def __add__(self, other: ('Binomial', 'Bernoulli')):
        # Given X~B(n,p), Y~(m,p) independents => X + Y ~ B(n+m, p)
        return Binomial(self.n + other.n, self.p)

    def __sub__(self, other: ('Binomial', 'Bernoulli')):
        # Difference of independents Binomial's variable := (X~B(n,p) - Y~B(m,p)) ~ B(n-m, p)
        return Binomial(self.n - other.n, self.p)

    def __str__(self):
        # Print X ~ B(n, p)
        return f'X ~ B(n={self.n}, p={self.p})'

    def __iter__(self):
        # Return binomial distribution as an array of bernoulli independent variable
        return [bernoulli.Bernoulli(self.p) for i in range(self.n)]

    def pmfshape(self, span, *args, **kwargs):
        # Plot mass probability function on a stick graphic
        return super().pmfshape(span, *args, **kwargs)
	
    def cdfshape(self, span, *args, **kwargs):
        # Plot distribution probability function on curved graphic
        return super().cdfshape(span, *args, **kwargs)

    def evshape(self, span, *args, **kwargs):
        # Plot expected value on a dashed line
        super().evshape(span, *args, **kwargs)


        

    