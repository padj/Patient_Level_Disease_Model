# IBM of shame based on https://arxiv.org/pdf/1702.03252.pdf
# Markov-esque model

# Heterogeneous population of individuals (sex, age), with three disease
# states: asymptomatic (PRE), sympomatic (SYMP), and dead (DEATH). 
# Transition between states is dictated by probability distributions. 

# P = [C0,          prob_disease_base,  prob_death_allCauses
#      prob_cured,  C1,                 prob_death_symp
#      0,           0,                  1]

# Disease states:
    #PRE - Asymptomatic state; Before the symptomatic state, when treatment 
    # can still be provided.
    
    #SYMP - Symptomatic state; Symptomatic disease, after being ashamed. 
    # With degraded health, high hospital costs and increased probability of 
    # dying of shame
    
    #DEATH - End state, Absorbing state, death by natural causes or because of
    # shame. 

# Treatment not yet implemented. 
#%%

import random 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%% CLASSES
class individual(object):
    def __init__(self, ID, mean, std):
        self.id = ID
        self.sex = random.sample(['M','F'], 1)
        self.age = int(np.random.normal(mean, std))
        self.stateTime = 0
        self.p_disease_base = 0.1      # Become ashamed (PRE -> SYMP)
        self.p_cured = 0.01             # spotaneous cure (SYMP -> PRE)
        self.state = 'PRE'
                  
    def calcDeathAllCause(self):
        if self.sex == 'M':
            self.p_death_allCause = maleMortality.at[self.age,str(currentYear)]
        else:
            self.p_death_allCause = femaleMortality.at[self.age,str(currentYear)]
    
    def calcDeathDisease(self):
        # Some function of state_time and fake Kaplan-Meier curve
        t = self.stateTime
        A = 0.002                       # coefficients for 
        B = -0.0438                     # third order polynomial
        C = 0.3119                      # describing K-M curve.
        D = 0
        self.p_death_disease = A*t**3 + B*t**2 + C*t**1 + D
            
    def calcDeathSymp(self):
        self.p_death_symp = (1 - (1-self.p_death_allCause) * 
                                (1-self.p_death_disease))

    def calcPmatrix(self):
        self.calcDeathAllCause()
        self.calcDeathDisease()
        self.calcDeathSymp()
        self.p_c0 = 1 - (self.p_disease_base + self.p_death_allCause)
        self.p_c1 = 1 - (self.p_cured + self.p_death_symp)
        #print('Pmatrix Calculated')
        
def PRE_transfer(idv):
    stay = idv.p_c0
    progress = idv.p_disease_base
    roll = random.uniform(0,1)
    if roll <= stay:
        pass # Nothing happens
    elif roll <= stay+progress:
        idv.state = 'SYMP'
        SYMP.append(idv.id)
        PRE.remove(idv.id)
    else:
        idv.state = 'DEATH'
        DEATH.append(idv.id)
        PRE.remove(idv.id)

def SYMP_transfer(idv):
    revert = idv.p_cured
    stay = idv.p_c1
    roll = random.uniform(0,1)
    if roll <= revert:
        idv.state = 'PRE'
        idv.stateTime = 0
        PRE.append(idv.id)
        SYMP.remove(idv.id)
    elif roll <= revert+stay:
        idv.stateTime += 1
    else:
        idv.state = 'DEATH'
        DEATH.append(idv.id)
        SYMP.remove(idv.id)
        
def updateHistory():
    PRE_history.append(len(PRE)/nPop*100)
    SYMP_history.append(len(SYMP)/nPop*100)
    DEATH_history.append(len(DEATH)/nPop*100)
    
def updatePopAges():
    for i in PRE:
        population[i].age += 1
    for i in SYMP:
        population[i].age += 1

#%% Initialise
PRE = []
SYMP = []
DEATH = []

PRE_history = []
SYMP_history = []
DEATH_history = []

maleMortality = pd.read_csv('../data/ONS_mortalities_male_parsed.csv')
femaleMortality = pd.read_csv('../data/ONS_mortalities_female_parsed.csv')

nPop = 10000
meanAge = 50
stdAge = 2
population = []
for i in range(nPop):
    population.append(individual(i,meanAge,stdAge))
    PRE.append(i)

updateHistory()

#%% Run

startYear = 1981
currentYear = startYear
Tmax = 37 # Total years
t = 0

while t < Tmax:
    for j in range(nPop):   # For each individual in the population         
        population[j].calcPmatrix() # Calculate the P matrix for the individual
        
        if population[j].state == 'PRE':    # If individual state is PRE:
            PRE_transfer(population[j])
        
        elif population[j].state == 'SYMP': # If individual state is SYMP:
            SYMP_transfer(population[j])
        
        else:
            pass
    
    updatePopAges()
    
    updateHistory()
           
    t += 1
    currentYear += 1


#%% PLOT

plt.figure(1)
plt.plot(PRE_history)
plt.plot(SYMP_history)
plt.plot(DEATH_history)
plt.xlabel('Time (years)')
plt.ylabel('Percentage of Population (%)')    
plt.axis([0, Tmax, 0, 100])
plt.legend(['Healthy', 'Symptomatic', 'Dead'])
plt.title('Healthy, symptomatic, and dead within the population against time for nPop = %s, meanAge = %s, and stdAge = %s.'%(nPop,meanAge,stdAge))
plt.grid(True)
