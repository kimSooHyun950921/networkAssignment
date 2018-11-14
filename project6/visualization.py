import matplotlib.pyplot as plt

value1 = [82,76,24,40,67,62,75]
value2 = [62,5,91,25,36,32,96,95,3,90,95,32,27,55]
value3 = [23,89,12,78,72,31,25,52]

box_plot_data = [value1,value2,value3]

plt.boxplot(box_plot_data)
plt.show()
