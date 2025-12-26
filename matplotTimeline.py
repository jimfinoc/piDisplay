import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import MultiCursor

from stockDataFunctions import return_details
from stockDataFunctions import return_positions
from stockDataFunctions import return_orders

displayStock = 'T'
# all_option_dates = return_details("All_stock_option_dates")[displayStock]
# print("all_option_dates")
# print(all_option_dates)

# Define the layout using a multi-line string
mosaic = """
         BBAAA
         CCAAA
         """

# Create the figure and axes
plt.style.use('dark_background')
fig, axd = plt.subplot_mosaic(mosaic, layout="constrained")
# plt.figure(facecolor='aliceblue')


# Plot data on each axes using the dictionary keys
axd['A'].plot(np.arange(0, 10), np.sin(np.arange(0, 10)), 'tab:blue')
axd['A'].set_title('Future Options')

axd['B'].plot(np.arange(0, 10), np.cos(np.arange(0, 10)), 'tab:orange')
axd['B'].set_title('Event History')

axd['C'].plot(np.arange(0, 10), np.tan(np.arange(0, 10)), 'tab:green')
axd['C'].set_title('Bollinger Bands')

if 'D' in mosaic:
    axd['D'].plot(np.arange(0, 10), np.arange(0, 10)**2, 'tab:red')
    axd['D'].set_title('Bollinger and Events')

for each in axd:
    axd[each].set_ylabel('Price ($)')
    axd[each].set_xlabel('Date')

# multi = MultiCursor(None, (axd['A'], axd['B'], axd['C'], axd['D']), color='r', lw=1, horizOn=True, vertOn=False)
multi2 = MultiCursor(None, (axd['A'], axd['B'], axd['C']), color='w', lw=1, horizOn=True, vertOn=True)


# Add a title for the entire figure
fig.suptitle('Basic Mosaic Layout Example')

plt.show()
