import matplotlib.pyplot as plt
import numpy as np

class Plot():
    def make_example_plot(x_axis_title = "undefined"):
        fig, ax = plt.subplots()
        ax.plot([1,2,3,None], [10, 3, 6, 9], marker="o")
        ax.set_title(f"Plot of {x_axis_title}")
        ax.set_xlabel(x_axis_title)
        ax.set_ylabel("Criminals")
        return fig
    
    def make_histogram(x_axis_title = "undefined"):
        x = np.random.normal(170, 10, 250)

        fig, ax = plt.subplots()
        ax.hist(x)
        ax.set_title("Histogram")
        ax.set_xlabel(x_axis_title)
        ax.set_ylabel("Density of criminals")
        return fig