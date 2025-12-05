import matplotlib.pyplot as plt
import numpy as np

import json
from pprint import pprint

d = {}

# def unwrap(keyword):
#     global d
#     with open("api_client/data_file.json") as json_data:
#         d = json.loads(json_data.read())
#         json_data.close()
#         pprint(d.get("total"))

class Plot():
    def make_example_plot(x_axis_title = "undefined"):
        fig, ax = plt.subplots()
        ax.plot([1,2,3,None], [10, 3, 6, 9], marker="o")
        ax.set_title(f"Plot of {x_axis_title}")
        ax.set_xlabel(x_axis_title)
        ax.set_ylabel("Criminals")
        return fig
    
    def make_histogram(x_axis_title = "undefined"):
        # unwrap("")
        x = np.random.normal(170, 10, 250)
        x = ["US", "US", "US", "US", "US", "CA", "CA", "MEX", "MEX", "MEX"]
        # ages = unwrap("ages")
        fig, ax = plt.subplots()
        ax.hist(x)
        ax.set_title("Histogram")
        ax.set_xlabel(x_axis_title)
        ax.set_ylabel("Density of criminals")
        return fig