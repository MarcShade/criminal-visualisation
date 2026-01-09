import matplotlib.pyplot as plt
import numpy as np

from api import Data
from pprint import pprint
from collections import Counter

# def unwrap(keyword):
#     global d
#     with open("api_client/data_file.json") as json_data:
#         d = json.loads(json_data.read())
#         json_data.close()
#         pprint(d.get("total"))

dropdown_to_hist = {
    "Weight": "weight",
    "Nationality": "nationalities",
    "Sex": "sex_id",
    "Country of Birth": "country_of_birth_id",
    "Languages Spoken": "languages_spoken_ids",
    "Height": "height",
    "Eye color": "eyes_colors_id"
}

def smart_add(lst, x):
    if isinstance(x, (list, tuple)):  # check if iterable
        lst.extend(x)
    else:
        lst.append(x)

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
    
    # def make_histogram(self, params = "nationalities"):
    #     nationalities = []
    #     for entries in self.data:
    #         if entries[params] == None or entries[params] == 0:
    #             continue
    #         # nationalities.append(entries[params])
    #         smart_add(nationalities, entries[params])
    #     # ages = unwrap("ages")
    #     fig, ax = plt.subplots()
    #     ax.hist(nationalities)
    #     ax.set_title("Histogram")
    #     ax.set_xlabel(params.capitalize())
    #     ax.set_ylabel("Density of criminals")
    #     return fig

    def make_histogram(self, selected):
        params = dropdown_to_hist[selected]
        values = []

        for entry in self.data:
            val = entry.get(params)

            if val in (None, 0):
                continue

            # If the value is a list (e.g. languages_spoken_ids)
            if isinstance(val, list):
                for item in val:
                    if item not in (None, 0):
                        values.append(item)
            else:
                values.append(val)

        # Decide plot type
        if all(isinstance(v, (int, float)) for v in values):
            fig, ax = plt.subplots()
            ax.hist(values, bins=20)
            ax.set_ylabel("Frequency")

        else:
            counts = Counter(values).most_common()
            labels, freqs = zip(*counts)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(labels, freqs)
            ax.tick_params(axis='x', rotation=45)
            ax.set_ylabel("Count")

        selected
        ax.set_title(f"{selected} distribution over criminals")
        ax.set_xlabel(selected)

        fig.tight_layout()
        return fig
