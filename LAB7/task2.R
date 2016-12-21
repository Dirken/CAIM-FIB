# #leemos el grafo
library("igraph")
g<-read.graph("/home/dirken/Downloads/session7networks/edges.txt", format="edgelist", directed=FALSE) 

ecount(g) #aristas
vcount(g) #vertices
V(g)
diameter(g)
transitivity(g) 
degree.distribution(g) 
hist(degree(g),breaks=40) 

#Grafo con tamaño de los nodos proporcional al pageRank
c=(page.rank(g)$vector)*100
plot(g,vertex.size=c)
#deteccion de comunidades
gc<-label.propagation.community(g)
gc #para ver los grupos
plot(g,vertex.color=membership(gc))
hist(membership(gc),breaks=18)
