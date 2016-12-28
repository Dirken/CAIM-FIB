#!/usr/bin/env python

"""
Simple module implementing LSH
"""

__version__ = '0.2'
__author__  = 'marias@cs.upc.edu'

import numpy
import sys
import argparse
import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed


class lsh(object):
    """
    implements lsh for digits database in file 'images.npy'
    """  
    
    def __init__(self, k, m):
        """ k is nr. of bits to hash and m is reapeats """
        # data is numpy ndarray with images
        self.data = numpy.load('images.npy')
        self.k = k
        self.m = m

        # determine length of bit representation of images
        # use conversion from natural numbers to unary code for each pixel,
        # so length of each image is imlen = pixels * maxval
        self.pixels = 64
        self.maxval = 16
        self.imlen = self.pixels * self.maxval

        # need to select k random hash functions for each repeat
        # will place these into an m x k numpy array
        numpy.random.seed(12345)
        self.hashbits = numpy.random.randint(self.imlen, size=(m, k))

        # the following stores the hashed images
        # in a python list of m dictionaries (one for each repeat)
        self.hashes = [dict()] * self.m

        # now, fill it out
        self.hash_all_images()

        return
    

    def hash_all_images(self):
        """ go through all images and store them in hash table(s) """
        # Achtung!
        # Only hashing the first 1500 images, the rest are used for testing
        for idx, im in enumerate(self.data[:1500]):
            for i in range(self.m):
                str = self.hashcode(im, i)

                # store it into the dictionary.. 
                # (well, the index not the whole array!)
                if str not in self.hashes[i]:
                    self.hashes[i][str] = []
                self.hashes[i][str].append(idx)
        return


    def hashcode(self, im, i):
        """ get the i'th hash code of image im (0 <= i < m)"""
        pixels = im.flatten()
        row = self.hashbits[i]
        str = ""
        for x in row:
            # get bit corresponding to x from image..
            pix = int(x) / int(self.maxval)
            num = x % self.maxval
            if (num <= int(pixels[int(pix)])):
                str += '1'
            else:
                str += '0'
        return str


    def candidates(self, im):
        """ given image im, return matching candidates (well, the indices) """
        res = set()
        for i in range(self.m):
            code = self.hashcode(im, i)
            if code in self.hashes[i]:
                res.update(self.hashes[i][code])
        return res

def distance(img1, img2):
    totalDistance = 0.
    img = img1 - img2
    for i in img:
        for j in i:
            totalDistance = totalDistance + j
    if (totalDistance < 0):
        totalDistance = totalDistance - 2*totalDistance 
    return totalDistance

def bruteForceSearch(me, i):
    lowdist = distance(me.data[i], me.data[0])
    image_res = 0
    for r in range(1, 1499):
        d = distance(me.data[i], me.data[r])
        if(d < lowdist):
            lowdist = d
            image_res = r              
    return image_res

def nearestNeighborSearch(me, i, cands):
    im = me.data[i]
    c = 0;
    image_res = -1;
    for r in cands:
        if(r != i):
            d = distance(im, me.data[r])
            if(c == 0):
                lowdist = d
                image_res = r
                c += 1;
            elif(d < lowdist):
                lowdist = d
                image_res = r              
    return image_res

@timeit
def main(argv=None):
    #JP
    ks = [20, 50, 100, 500, 750, 1000, 1250, 1500, 1750, 2000]
    ms = [5, 10, 15, 25, 50, 75, 100, 125, 150, 200]
    it = 9
    while it < 10:
        ts = time.time()
        parser = argparse.ArgumentParser()
        # parser.add_argument('-k', default=ks[it], type=int)
        # parser.add_argument('-m', default=ms[it], type=int)
        parser.add_argument('-k', default=50, type=int)
        parser.add_argument('-m', default=5, type=int)
        args = parser.parse_args()
        print "Running lsh.py with parameters k =", args.k, "and m =", args.m
        print
        me = lsh(args.k, args.m)

        # show candidate neighbors for first 10 test images
        for r in range(1500,1510):
            im = me.data[r]
            cands = me.candidates(im)
            bf = bruteForceSearch(me,r)
            ne = nearestNeighborSearch(me,r,cands)
            print "There are", len(cands), "candidates for image", r
            print "Difference between nearest neighbour VS brute-force search for", r, "is:", distance(me.data[ne],me.data[bf])
            print "Brute-force search for", r, "is", bf
            print "Nearest neighbour for", r, "is", ne
            print
        te = time.time()
        print ('%2.2f sec' % (te - ts))
        it += 1
    return

if __name__ == "__main__":
  sys.exit(main())
