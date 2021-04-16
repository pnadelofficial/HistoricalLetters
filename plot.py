import cartopy
import cartopy.crs as ccrs
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


def geodetic_crop(geodetic_coords, padding=5):
    min_coord = np.min(geodetic_coords, axis=0) - padding
    max_coord = np.max(geodetic_coords, axis=0) + padding
    return min_coord, max_coord


def plot_geodetic(loc_to_geodetic, sorted_unique_locs, loc_to_count,
                  min_coord=None, max_coord=None):
    # get names and geodetics for plotting
    locs = np.asarray(list(loc_to_geodetic.keys()))
    # TODO fix coords layout
    geodetic_coords = np.asarray(list(loc_to_geodetic.values()))
    geodetic_coords = geodetic_coords[:, [1, 0]]
    # remove any locations from geodetic that was not in parser
    loc_in_parser = np.isin(locs, sorted_unique_locs)
    locs = locs[loc_in_parser]
    geodetic_coords = geodetic_coords[loc_in_parser]
    # count occurences of each location in parser
    loc_counts = np.asarray([loc_to_count[loc] for loc in locs])
    # set up figure and axes
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    # zoom view around points
    if min_coord is None:
        min_coord, _ = geodetic_crop(geodetic_coords)
    if max_coord is None:
        _, max_coord = geodetic_crop(geodetic_coords)
    ax.set_extent([min_coord[0], max_coord[0], min_coord[1], max_coord[1]],
                  crs=ccrs.PlateCarree())
    # add imagery
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.OCEAN)
    # plot points
    sc = plt.scatter(geodetic_coords[:, 0], geodetic_coords[:, 1], color='#00000088', marker='o',
                     s=2*loc_counts, transform=ccrs.PlateCarree())
    return locs, sc, fig, ax


def plot_geodetic_annotated(loc_to_geodetic, sorted_unique_locs, loc_to_count):
    locs, sc, fig, ax = plot_geodetic(loc_to_geodetic, sorted_unique_locs, loc_to_count)
    # create annotation
    # code modified from:
    # https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    # define func to update annotations
    def update_annot(ind):
        # get position from first point
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        # draw box with annotations from all points from event
        text = "\n".join([locs[n] for n in ind["ind"]])
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)

    # define func to handle clicking
    def on_click(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            # update annotation if point with data clicked
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            # hide annotation if point without data clicked
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
    fig.canvas.mpl_connect("button_release_event", on_click)


def plot_geodetic_anim(loc_to_geodetic, parser):
    # TODO fix coords layout
    geodetic_coords = np.asarray(list(loc_to_geodetic.values()))
    geodetic_coords = geodetic_coords[:, [1, 0]]
    min_coord, max_coord = geodetic_crop(geodetic_coords)
    # set up figure and axes
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    # zoom view around points
    ax.set_extent([min_coord[0], max_coord[0], min_coord[1], max_coord[1]],
                  crs=ccrs.PlateCarree())
    # add imagery
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.OCEAN)
    sc = plt.scatter([], [], color='#00000088', marker='o')

    def update_plot(date):
        # filter locations by date
        locations = parser.dateline_locs[parser.dateline_dates == date]
        sorted_unique_locs, unique_loc_counts = parser.unique(
            locations, return_counts=True
        )
        loc_to_count = dict(zip(sorted_unique_locs, unique_loc_counts))
        # get names and geodetics for plotting
        locs = np.asarray(list(loc_to_geodetic.keys()))
        # remove any locations from geodetic that was not in parser
        loc_in_parser = np.isin(locs, sorted_unique_locs)
        locs = locs[loc_in_parser]
        parsed_geodetic_coords = geodetic_coords[loc_in_parser]
        # count occurences of each location in parser
        loc_counts = np.asarray([loc_to_count[loc] for loc in locs])
        # update the plot
        sc.set_offsets(parsed_geodetic_coords)
        sc.set_sizes(2*loc_counts)
        plt.title(date)
        return sc,
    # don't remove reference to animation before it is shown!
    ani = FuncAnimation(fig, update_plot, frames=parser.unique_dates)
    plt.show()
