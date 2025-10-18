import matplotlib.pyplot as plt
import pandas as pd

# Load data from experiments.csv
df = pd.read_csv('../results/experiments.csv')

# Filter for completed runs (no N/A)
df = df[df['wall_time_s'] != 'N/A']

# Plot digits/s vs chunk for different workers
fig, ax = plt.subplots()
for workers in df['workers'].unique():
    subset = df[df['workers'] == workers]
    ax.plot(subset['chunk'], subset['digits_per_s'], label=f'Workers: {workers}', marker='o')

ax.set_xlabel('Chunk Size')
ax.set_ylabel('Digits/s')
ax.set_title('Digits/s vs Chunk Size')
ax.legend()
plt.savefig('../figs/scaling.png')
plt.show()
