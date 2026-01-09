import matplotlib.pyplot as plt
import numpy as np

from api_client.api_client import Data
from pprint import pprint

d = {}

# def unwrap(keyword):
#     global d
#     with open("api_client/data_file.json") as json_data:
#         d = json.loads(json_data.read())
#         json_data.close()
#         pprint(d.get("total"))


def smart_add(lst, x):
    if isinstance(x, (list, tuple)):  # check if iterable
        lst.extend(x)
    else:
        lst.append(x)

data = {}

class Plot():
    def __init__(self):
        self.data = Data.get_data()

    def make_example_plot(x_axis_title = "undefined"):
        fig, ax = plt.subplots()
        ax.plot([1,2,3,None], [10, 3, 6, 9], marker="o")
        ax.set_title(f"Plot of {x_axis_title}")
        ax.set_xlabel(x_axis_title)
        ax.set_ylabel("Criminals")
        return fig
    
    def make_histogram(self, params = "nationalities"):
        nationalities = []
        for entries in self.data:
            if entries[params] == None or entries[params] == 0:
                continue
            # nationalities.append(entries[params])
            smart_add(nationalities, entries[params])
        # ages = unwrap("ages")
        fig, ax = plt.subplots()
        ax.hist(nationalities)
        ax.set_title("Histogram")
        ax.set_xlabel(params.capitalize())
        ax.set_ylabel("Density of criminals")
        return fig