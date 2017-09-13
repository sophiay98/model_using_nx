import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# initiate all the nodes
def initiate(g):
    n=0
    while n<=g.number_of_nodes()-1:
        g[n]['infected']={'state':False, 'duration':0}
        g[n]['recovered']={'state':False, 'duration':0}
        g[n]['susceptible']={'state':True, 'duration':0}
        susceptible_individuals.append(n)
        n+=1
    individual_immunity(g,48,16)
    

#normal distribution
def individual_immunity(g,mean,sd):
	nodes=g.nodes()
	for node in g:
		g[node]['immunization_degree']=int(np.random.normal(mean,sd))


'''change????'''
# randomly select x to infect
# x in the number of nodes that got infected initially
def first_infection(x,g):
    while x > 0:
        n = random.randint(0, g.number_of_nodes() - 1)
        if g[n]['infected']['state']:
            first_infection(1, g)
        else:
            g[n]['infected']['state'] = True
            infected_individuals.append(n)
            susceptible_individuals.remove(n)
        x -= 1
    
	#i=0
    #while i < len(infected_individuals): 
	    #print g.degree(infected_individuals[i])
	    #i+=1
	    
#kill signal
#every infected node will have (50+g[n][immunization_degree])^2/100 probability of sending kill signal to the herd
def kill_signal(n):
	rand=random.randint(0,100)
	if rand < (g[n]['immunization_degree'])^2/100:
		g[n]['infected']={'state':False, 'duration':0}
		g[n]['recovered']={'state':True, 'duration':0}
		if n in infected_individuals:
			infected_individuals.remove(n)
		recovered_individuals.append(n)
		set_susceptibleneighbors=set(g.neighbors(n))&set(susceptible_individuals)
		set_infectedneighbors=set(g.neighbors(n))&set(infected_individuals)
		for neighbor in set_susceptibleneighbors:
			immunization(neighbor)
		for neighbor in set_infectedneighbors:
			increase_recover_rate(neighbor)
#+77 so that the node with the highest immunization_degree would have almost a 100% chance to send out kill signal upon infection
def immunization(n):
    rand=random.randint(0,100)
    if rand < ((g[n]['immunization_degree']-48)^2)/100+77:
    	g[n]['recovered']={'state':True, 'duration':0}
    	susceptible_individuals.remove(n)
    	recovered_individuals.append(n)
    	
'''recovers faster or becomes recovered?'''
def increase_recover_rate(n):
	rand=random.randint(0,100)
	if rand < ((g[n]['immunization_degree']-48)^2)/100+77:
		g[n]['infected']['duration']+=1

##Look at the neighbors of the infected node(s)
##Each susceptible neighbor is infected with probability beta; update status
##For the nodes that became infected in the PREVIOUS alpha time steps, update status
##to recovered
#beta,in percentage, determines how often a susceptible-infected contact results in a new infection. 
#gamma, in days, determined the time it takes for an infected individual to recover
'''should I do 1/gamma?'''
'''a=random.randint(0,100)+(g[neighbor]['immunization_degree']-48)^2/100????'''
def update(g, alpha, beta, gamma):
    temp_susceptible=susceptible_individuals
    temp_infected=infected_individuals[:]
    temp_recovered=recovered_individuals
    #print temp_infected, 'temp infected'
    #print len(temp_infected), 'initial infected'
    for x in temp_infected:
    	set_susceptibleneighbors=set(g.neighbors(x))&set(temp_susceptible)
        for neighbor in set_susceptibleneighbors:
        	a = random.randint(0,100)+((g[neighbor]['immunization_degree']-48)^2)/100
        	
        	if a <= beta:
        		g[neighbor]['infected']['state'] = True
    			infected_individuals.append(neighbor)
    			susceptible_individuals.remove(neighbor)
    			#kill_signal(neighbor)
        if g[x]['infected']['duration'] > gamma:
	       	g[x]['infected']['state']=False
	     	g[x]['infected']['duration']=0
         	g[x]['recovered']['state']=True
           	infected_individuals.remove(x)
        	recovered_individuals.append(x)
        else:
			g[x]['infected']['duration'] += 1
    for x in temp_recovered:
        a = random.randint(0, 100)
        if a <= alpha:
            g[x]['recovered']['duration'] += 1
        else:
            g[x]['recovered'] = {'state': False, 'duration': 0}
            recovered_individuals.remove(x)
            susceptible_individuals.append(x)
printfile = open("virus-b80-ks.txt", 'w')
j=0
while j<500:
	g = nx.Graph()
	infected_individuals = []
	susceptible_individuals = []
	recovered_individuals = []

	with open('email-Enron.txt') as f:
		for line in f:
			line = line.strip('\n').split('\t')
			head = int(line[0])
			tail = int(line[-1])
			g.add_edge(head, tail)
			
	initiate(g)
	initialInfected=5
	first_infection(initialInfected, g)
	print>>printfile,initialInfected,0,len(g.nodes())-initialInfected
	day=0
	while day<20:
		update(g,20,80,3)  #alpha,beta,gamma 
		infected=len(infected_individuals)
		recovered=len(recovered_individuals)
		susceptible=len(susceptible_individuals)
		print>>printfile,infected,recovered,susceptible
		day+=1
		print day
    
	


	"""Plot Infected, Recovered, Susceptible"""
# 	infecteds=[]
# 	susceptibles=[]
# 	recovereds=[]
# 	time=[]
# 	tempTime=0
# 	for line in file("virus.txt"):
# 		tempdata=line.split(None)
# 		infected=int(tempdata[0])
# 		recovered=int(tempdata[1])
# 		susceptible=int(tempdata[2])
# 		infecteds.append(infected)
# 		susceptibles.append(susceptible)
# 		recovereds.append(recovered)
# 		time.append(tempTime)
# 		tempTime+=1
	print ("round "+str(j))
	j+=1
printfile.close()
# #infected/time=red solid line
# #susceptible/time=yellow dashed line
# #recovered/time=green dotted line
# fig, ax=plt.subplots()
# ax.plot(time, infecteds, 'r-', label='infected/time')
# ax.plot(time, susceptibles, 'y--', label='susceptible/time')
# ax.plot(time, recovereds, 'g:',label='recovered/time')
# lgd = legend=ax.legend(loc='best', shadow='True')
# frame = legend.get_frame()
# frame.set_facecolor('0.90')
# plt.show()	
