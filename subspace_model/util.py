import builtins

import holoviews as hv
import pandas as pd
import plotly.io as pio

# Save the original print function
original_print = builtins.print


# Define a new print function
def print(*args, **kwargs):
    """
    Override the default print function such that dataframes are named.
    """
    for arg in args:
        if isinstance(arg, pd.DataFrame) and hasattr(arg, "name"):
            original_print(f"{arg.name}:")
            original_print(arg, **kwargs)
        else:
            original_print(arg, **kwargs)


# Make sure that plotly charts are displayed on github in jupyter notebooks
github_render = lambda hvplot_plotly_chart: pio.show(
    hv.render(hvplot_plotly_chart, backend="plotly")
)
g = lambda h: github_render(h)


import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def get_hex_colors_from_matplotlib_cmap(n, cmap_name):
    cmap = plt.get_cmap(cmap_name)
    colors = cmap(np.linspace(0, 1, n))
    hex_colors = [matplotlib.colors.to_hex(color) for color in colors]
    return hex_colors


import ipynbname


def hv_save(plot, plot_name: str, nb_name: str):
    plot_file = f"images/{nb_name}-{plot_name}.png"
    print(f"Saving plot to {plot_file}...")
    hv.save(plot, plot_file, fmt="png")


if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df.name = "MyDataFrame"

    print(df)  # This will print the name of the DataFrame and then the DataFrame itself
    print("Hello, World!")  # This will print normally
