import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import csv

f = open('voc_growth_reverse.csv','r') # Or voc_growth.csv :in order parsed files
i=0
xdata =[]
ydata = []
for line in f:
	if(i==0):
		i=1
		continue
	parts = line.split(',')
	xdata.append(int(parts[1]))
	ydata.append(int(parts[2].strip()))
f.close()
# print len(xdata)
# print len(ydata)
xx= np.array(xdata)
yy= np.array(ydata)
p0 =  np.array([1,1])

def my_fun(par,x,y):
	return  y-par[0]*np.power(x,par[1])

def fun_eval(par,x):
	return  par[0]*np.power(x,par[1])

# print 1*p0[0]
result = leastsq(my_fun,p0[:],args=(xx,yy))
f = open('fit.csv','w+')
writer = csv.writer(f)
for x in xx:
	writer.writerow((x,fun_eval(result[0],x)))
k,b = result[0]
print "k = "+str(k),
print "b = "+str(b)
f.close()