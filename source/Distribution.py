	
'''

With thanks to Eelco Hoogendoorn for this helpful post on inverse transform sampling: https://stackoverflow.com/questions/21100716/fast-arbitrary-distribution-random-sampling and the code below!

This code implements the sampling of n-d discrete probability distributions. By setting a flag on the object, it can also be made to be used as a piecewise constant probability distribution, which can then be used to approximate arbitrary pdf's. Well, arbitrary pdfs with compact support; if you efficiently want to sample extremely long tails, a non-uniform description of the pdf would be required. But this is still efficient even for things like airy-point-spread functions (which I created it for, initially). The internal sorting of values is absolutely critical there to get accuracy; the many small values in the tails should contribute substantially, but they will get drowned out in fp accuracy without sorting.

Example usage given:

x = np.linspace(-100, 100, 512)
p = np.exp(-x**2)
pdf = p[:,None]*p[None,:]     #2d gaussian
dist = Distribution(pdf, transform=lambda i:i-256)
print dist(1000000).mean(axis=1)    #should be in the 1/sqrt(1e6) range
import matplotlib.pyplot as pp
pp.scatter(*dist(1000))
pp.show()

'''

import numpy as np

class Distribution(object):
    """
    draws samples from a one dimensional probability distribution,
    by means of inversion of a discrete inversion of a cumulative density function

    the pdf can be sorted first to prevent numerical error in the cumulative sum
    this is set as default; for big density functions with high contrast,
    it is absolutely necessary, and for small density functions,
    the overhead is minimal

    a call to this distibution object returns indices into density array
    """
    def __init__(self, pdf, sort = True, interpolation = True, transform = lambda x: x):
        self.shape          = pdf.shape
        self.pdf            = pdf.ravel()
        self.sort           = sort
        self.interpolation  = interpolation
        self.transform      = transform

        #a pdf can not be negative
        assert(np.all(pdf>=0))

        #sort the pdf by magnitude
        if self.sort:
            self.sortindex = np.argsort(self.pdf, axis=None)
            self.pdf = self.pdf[self.sortindex]
        #construct the cumulative distribution function
        self.cdf = np.cumsum(self.pdf)
    @property
    def ndim(self):
        return len(self.shape)
    @property
    def sum(self):
        """cached sum of all pdf values; the pdf need not sum to one, and is imlpicitly normalized"""
        return self.cdf[-1]
    def __call__(self, N):
        """draw """
        #pick numbers which are uniformly random over the cumulative distribution function
        choice = np.random.uniform(high = self.sum, size = N)
        #find the indices corresponding to this point on the CDF
        index = np.searchsorted(self.cdf, choice)
        #if necessary, map the indices back to their original ordering
        if self.sort:
            index = self.sortindex[index]
        #map back to multi-dimensional indexing
        index = np.unravel_index(index, self.shape)
        index = np.vstack(index)
        #is this a discrete or piecewise continuous distribution?
        if self.interpolation:
            index = index + np.random.uniform(size=index.shape)
        return self.transform(index)


if __name__=='__main__':
    shape = 3,3
    pdf = np.ones(shape)
    pdf[1]=0
    dist = Distribution(pdf, transform=lambda i:i-1.5)
    print dist(10)
    import matplotlib.pyplot as pp
    pp.scatter(*dist(1000))
    pp.show()


