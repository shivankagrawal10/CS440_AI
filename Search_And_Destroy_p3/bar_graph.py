import matplotlib.pyplot as plt
import numpy as np

strats = ['Basic Agent 1', 'Basic Agent 2', 'Improved Agent 3']
scores = [1151.95, 1025.12,  975.75]


ypos = np.arange(len(strats))
plt.xticks(ypos, strats)
plt.bar(ypos, scores)
plt.xlabel('Search Method')
plt.ylabel('Average Final Score')
plt.title('Average Results for 100 Rounds\nof Search and Destroy with Bonus Information')
plt.show()