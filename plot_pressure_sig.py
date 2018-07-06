'''
Test reading pressure signature from .csv
'''

import matplotlib.pyplot as plt
import csv
import pickle
import numpy as np

def getPressureSig(fignum, color):
    '''getFlightPlan takes the figure number and color as string
    inputs and outputs lists of data from the .csv file.
    '''
    filename = fignum + '-' + color + '.csv'
    
    delta_p = []
    dist = []
    with open('Pressure_Signature_Files/' + filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            dist.append(row[0])
            delta_p.append(row[1])
            
    # changing flight plan data to floats and making dist meters
    for i in range(len(dist)):
        delta_p[i] = float(delta_p[i])
        dist[i] = float(dist[i])
    
    return dist, delta_p

    
x = []
y = []    
nearfield_sig = pickle.load(open("nearfiled_signature.p","rb"))
for i in range(len(nearfield_sig)):
    # print(nearfield_sig[i])
    x.append(nearfield_sig[i][0])
    y.append(nearfield_sig[i][1])
   
dist, delta_p = getPressureSig('7.41','Red')
double_list = []
for i in range(len(dist)):
    dist[i] = dist[i] + 150
    #dist[i] = dist[i] / 12
    double_list.append([dist[i], delta_p[i]])
double_list = np.array(double_list)
 
g = open("n2_signature.p","wb")
pickle.dump(double_list,g)
g.close()

plt.plot(dist,delta_p)
plt.plot(x,y)
plt.show()

