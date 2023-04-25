#!/usr/bin/env python
# coding: utf-8

# In[2]:


from qiskit import *
from numpy.random import randint
import numpy as np

Raw_key_len = 5
##########FUNCTIONS###############
##The creation of qc depending on alice base
def alice_preperation(alice_bit, alice_base):
    qc = QuantumCircuit(1,1)
    #Base X
    if alice_base == 0:
        if alice_bit == 0:
            pass
        else:
            qc.x(0) #Pauli_gate X
    #Base Z
    else:
        if alice_bit == 0:
            qc.h(0)
        else:
            qc.x(0)
            qc.h(0)
    qc.barrier()
    return qc

##It applies to the coded message the bases that bob choose
def measure_code (bob_bases, code_message):
    measured_bit =[]
    if bob_bases == 0:
        code_message.measure(0,0)
    else:
        code_message.h(0)
        code_message.measure(0,0)
    aer_sim = Aer.get_backend('aer_simulator')     
    qobj = assemble(code_message, shots=1, memory=True)
    result = aer_sim.run(qobj).result()
    measured_bit = int(result.get_memory()[0])
    return measured_bit


##When Eve insert
def Eve_interference(eve_bases, code_message):
    measured_bit = []
    if eve_bases == 0:
        code_message.measure(0,0)
    else:
        code_message.h(0)
        code_message.measure(0,0)
    aer_sim = Aer.get_backend('aer_simulator')     
    qobj = assemble(code_message, shots=1, memory=True)
    result = aer_sim.run(qobj).result()
    measured_bit = int(result.get_memory()[0])
    return alice_preperation(measured_bit, eve_bases)



##It removes bases that are different
def remove_bases (alice_bases, bob_bases, bit):
    if alice_bases == bob_bases:
        return bit
    
#########BOB_PART#########
##Bobs random bases
def Bob_actions():
    ##Compare Bobs bases with the bases alice sended
    for i in range(n):
        Bob_results.append(measure_code(Bob_bases[i], code_message[i]))
       
def protocol_BB84():    
    ###########ALICE PART#############
    np.random.seed()
    n= 100

    #random generation of alice bits
    Alice_bits=[]
    for i in range(n):
        Alice_bits.append(randint(0,2))

    #random generation of alice bases
    ## Base X is 0 and base Z is 1
    Alice_bases=[]
    for i in range(n):
        Alice_bases.append(randint(0,2))

    #Base placement on alice qubits
    code_message= []
    for i in range(n):
        code_message.append(alice_preperation(Alice_bits[i], Alice_bases[i]))
        

#for i in range(n):
    #code_message[0].draw(output='mpl')

    
    ########EVE_PART########
    ##Eve operates randomly
    ##If random number = 1 Eve operates
    Eve_bases=[]
    Eve_results = []
    for i in range(n):
        Eve_bases.append(randint(0,2))
    ##Compare Bobs bases with the bases alice sended
    for j in range(n):
        Eve_results.append(Eve_interference(Eve_bases[j], code_message[j])) 
   
        
        
    ########BOB_PART########
    ##Bob random bases
    Bob_bases=[]
    Bob_results = []
    Bob_key= []
    for i in range(n):
        Bob_bases.append(randint(0,2))
    ##Compare Bobs bases with the bases alice sended
    ##Two cases
    for j in range(n):
        Bob_results.append(measure_code(Bob_bases[j], Eve_results[j]))

    
    #######Checking bases #######
    ##Alice Key
    Alice_key = []
    Bob_key=[]
    for i in range(n):
        #Alice key
        if remove_bases(Alice_bases[i], Bob_bases[i], Alice_bits[i])!= None:
            Alice_key.append(remove_bases(Alice_bases[i], Bob_bases[i], Alice_bits[i]))
        
        #Bob_key
        if remove_bases(Alice_bases[i], Bob_bases[i], Bob_results[i])!= None:
            Bob_key.append(remove_bases(Alice_bases[i], Bob_bases[i], Bob_results[i]))   

    ##Test if the protocol works properly
    for i in range(Raw_key_len):
        key = randint(0, len(Alice_key))
        if Alice_key[i] != Bob_key[i]:
            #print("Intruder was detected")
            return 0
    return 1
    #if safe == 1 and rand== 1:
        #print("The algorithm failed to detect Eve")
        

n=100   
Raw_key_len = 0
Raw_key_list = []
for _ in range(20):
    fail = 0
    Raw_key_len += 1
    for i in range(n):
        fail += protocol_BB84()
    Raw_key_list.append(fail)
    
print(Raw_key_list)


# In[3]:


import matplotlib.pyplot as plt

samples = []
for k in range(20):
    samples.append(k+1)

# plotting the points 
plt.plot(samples,Raw_key_list)

plt.ylabel('Protection failed')
# naming the y axis
plt.xlabel('Raw_key_length')

plt.ylim(0,100)
plt.xlim(1,19)
# giving a title to my graph
plt.title('The probability of Eve not being detected')
  
# function to show the plot
plt.show()


# In[ ]:





# In[16]:


code_message[0].draw()


# In[17]:


code_message[1].draw()

