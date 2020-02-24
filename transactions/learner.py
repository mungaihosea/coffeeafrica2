import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_frame = pd.read_csv('cpus.csv')
print(data_frame)
x = data_frame['cpu speed(Ghz)'].values
y = data_frame['cost(USD)'].values
n = len(x)

x_reserve=  x
y_reserve = y

def model(xval = None):
	global x
	global y

	x_reserve=  x
	y_reserve = y

	mean_x = np.mean(x)
	mean_y = np.mean(y)

	n = len(x)
	a = 0
	b = 0
	# fomula
	for i in range(n):
		a = a + ((x[i] - mean_x)*(y[i]-mean_y))
		b = b + ((x[i] - mean_x)**2)
	m = a/b

	print('m =',m)
	print('y =',mean_y)
	print('x =',mean_x)
	c =(mean_y - (m*mean_x)) 

	print("c =",c)
	val_x = x
	val_y = []

	for item in val_x:
		y_val = (m*item) + c
		val_y.append(y_val)

	if xval != None:
		returnvar = (m*xval) + c
	else:
		returnvar = None
	# accuracy evaluation
	f = 0
	g = 0
	k = 0
	for val in val_y:
		f = f +((val - mean_y)**2)
		g = g +((y[k] - mean_y)**2)
		k += 1
	r2 = f/g

	print("accuracy of model prediction ---->",str(r2*100)+"%")
	print("\n")

	plt.plot(val_x,val_y, color = 'c', label = 'regression line')
	plt.xlabel('Cpu speed in Ghz')
	plt.ylabel('Price in USD')
	plt.scatter(x_reserve,y_reserve, color = 'r', label = 'scatter plot')

	return returnvar

def predict(cpu_frequency):
	val = model(cpu_frequency)
	return val

hold = input('Enter the cpu cpu_frequency to predict: ')
hold = float(hold)
price = predict(hold)
print("$"+ str(round(price,2)))

# data = data_frame.groupby('type').mean().sort_values(['cost(USD)'], ascending = False)
# print(data)

plt.scatter(hold,price,color = 'k', label = 'prediction')
plt.grid(True,color='g')
plt.title("Price range and cpu clock speed")
plt.legend()
plt.show()