import numpy as np
import pandas as pd


def loc_to_geodetic(fname):
    """Get location to geodetic coordinate dictionary from CSV

    Args:
        fname (str): Path to CSV to parse

    Returns:
        dict: Dictionary mapping location to geodetic coordinate
    """
    df = pd.read_csv(fname, usecols=[0, 1, 2])
    locs = df.iloc[:, 0].to_numpy()
    geodetics = df.iloc[:, 1:].to_numpy()
    has_geodetics = ~np.logical_or(np.isnan(geodetics)[:, 0], np.isnan(geodetics)[:, 1])
    locs = locs[has_geodetics]
    geodetics = geodetics[has_geodetics]
    loc_to_geodetic = {locs[i]: geodetics[i] for i in range(len(locs))}
    return loc_to_geodetic
