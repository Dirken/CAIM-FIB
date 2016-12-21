import igraph
import random
import matplotlib.pyplot as plot
import math 

def main():
    n = 1200
    iterations = 5

    probabilities = []
    averagePath = []
    transitivity = []
    g = igraph.Graph().Watts_Strogatz(1, n, 2, 0)
    averageValueZero = g.average_path_length()
    transivityValueZero = g.transitivity_undirected(igraph.TRANSITIVITY_ZERO)

    p = 0.9999
    while 0.00001 <= p :
        i = transivityAux = averagePathAux = 0
        while i < iterations:
            g = igraph.Graph().Watts_Strogatz(1, n, 2, p)
            asp = g.average_path_length()
            trans = g.transitivity_undirected(igraph.TRANSITIVITY_ZERO)
            averagePathAux = averagePathAux + asp
            transivityAux = transivityAux + trans
            i = i + 1

        probabilities.append(p)
        p = probabilities[len(probabilities)-1]/1.25
        averagePath.append(averagePathAux/iterations/averageValueZero)
        transitivity.append(transivityAux/iterations/transivityValueZero)

    fig, graphic = plot.subplots()
    graphic.plot(probabilities, averagePath)
    graphic.plot(probabilities, transitivity)

    plot.xscale('log')
    plot.show()

main()
