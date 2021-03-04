import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np


def plot_geodetic(geodetic_coords):
    # set up map imagery
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.COASTLINE)
    # ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
    # plot points
    for geodetic_coord in geodetic_coords:
        plt.plot(geodetic_coord[0], geodetic_coord[1], color='blue', marker='o',
                 transform=ccrs.PlateCarree())
    # zoom view around points
    min_coord = np.min(geodetic_coords, axis=1) - 5
    max_coord = np.max(geodetic_coords, axis=1) + 5
    ax.set_extent([min_coord[0], max_coord[0], min_coord[1], max_coord[1]],
                  crs=ccrs.PlateCarree())
    # display plot
    plt.show()
