import matplotlib.pyplot as plt
import numpy as np

from api import Data
from pprint import pprint

from collections import Counter
import geopandas as gpd

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
        if Data.needs_refresh():
            notices = Data.fetch_all_notices()
            Data.fetch_notice_details(notices)
            Data.save_data()
        self.data = Data.get_data()

    def make_world_map(self):
        values = []
        for entry in self.data:
            nat = entry.get("nationalities")
            if nat in (None, 0):
                continue
            if isinstance(nat, list):
                values.extend(nat)
            else:
                values.append(nat)

        counts = Counter(values)

        world = gpd.read_file(
            "data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
        )

        world["count"] = world["ISO_A2"].map(counts).fillna(0)

        world = world.to_crs("ESRI:54042")

        fig, ax = plt.subplots()
        world.plot(
            column="count",
            ax=ax,
            cmap="Reds",
            legend=True,
            legend_kwds={'orientation': 'horizontal', "label": "Number of criminals", "pad": 0},
            missing_kwds={"color": "#2b2b2b"}
        )
        
        ax.set_title("Criminal nationality distribution (world map)")
        ax.axis("off")

        fig.tight_layout()
        return fig

    def make_histogram(self, selected):
        params = dropdown_to_hist[selected]
        values = []

        for entry in self.data:
            val = entry.get(params)

            if val in (None, 0):
                continue

            if isinstance(val, list):
                for item in val:
                    if item not in (None, 0):
                        values.append(item)
            else:
                values.append(val)

        if all(isinstance(v, (int, float)) for v in values):
            fig, ax = plt.subplots()
            ax.hist(values, bins=20)

        else:
            counts = Counter(values).most_common()
            labels, freqs = zip(*counts)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(labels, freqs)
            ax.tick_params(axis='x', rotation=45)

        ax.set_title(f"{selected} distribution over criminals")
        ax.set_xlabel(selected)
        ax.set_ylabel("Count")


        fig.tight_layout()
        return fig
