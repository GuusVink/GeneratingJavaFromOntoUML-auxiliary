#  Copyright (c) 2024.
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots
plt.style.use(['science', 'scatter'])
import numpy as np

file_path = r'results/transformation_results 2024-10-21 12-57-22 Special Letters allowed.csv'

df = pd.read_csv(file_path)

# filter for successful transformation
df = df[df['transformation_successful']]

# filter outlier
n_class_threshold = 200
print(f"Models with more than {n_class_threshold} classes:\n\t {df[df['n_classes'] > n_class_threshold]['model'].values}")
df = df[df['n_classes'] <= n_class_threshold]


x = np.array(df['n_classes'])
y = np.array(df['transformation_time_s'])

x_smooth = np.arange(x.min() - 3, x.max() + 5, 5)
m, b = np.polyfit(x, y, 1)
print(f" Fitted line, m={m} and b={b}")

plt.figure(dpi=400)
plt.xlabel('Number of classes')
plt.ylabel('Execution time (s)')

plt.plot(x_smooth, m*x_smooth+b, c='black', alpha=0.3, marker='', linestyle='dashed')
plt.scatter(x, y, marker='+', c='#f15b54')
#
plt.tight_layout()
plt.show()

