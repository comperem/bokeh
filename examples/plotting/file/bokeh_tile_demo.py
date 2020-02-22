# Demonstrate Bokeh's various tile providers with medium-close-in zoom using
# modified tile_providers.py to include OSM, WIKIMEDIA, and ESRI_IMAGERY tile providers.
#
# Usage:
#   python3 bokeh_tile_demo.py


from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import Div
from bokeh.layouts import column, layout

output_file("foo.html")

# helper function for coordinate conversion between lat/lon in decimal degrees to web mercator
def LatLon_to_EN(lat_lon):
    from pyproj import Proj, transform
    lat=lat_lon[0]
    lon=lat_lon[1]
    try:
        #              from: WGS84, lat/lon, EPSG:4326    to: Web Mercator, EPSG:3857 in meters
        easting, northing = transform( Proj('epsg:4326'), Proj('epsg:3857'), lat, lon) # from WGS-84 to Web Mercator Easting/Northing
        return easting, northing # meters
    except:
        return None, None

description = Div(text="""<b><code>bokeh_tile_examples.py</code></b> - Bokeh tile provider examples. Linked Pan and Zoom on all maps!""")

# pick a location and generate a 4-point window around it: bottom-left, upper-right
map_center_lat_lon = ( 30.268801, -97.763347 ) # Lady Bird Lake, Austin Texas

dE = 1000 # (m) Easting  plus-and-minus from map center
dN = 1000 # (m) Northing plus-and-minus from map center
EN = LatLon_to_EN(map_center_lat_lon)
x_range = ( EN[0]-dE , EN[0]+dE ) # (m) Easting  x_lo, x_hi
y_range = ( EN[1]-dN , EN[1]+dN ) # (m) Northing y_lo, y_hi


plot=[0]*Vendors.__len__() # initialize list to store Vendor plots
idx=0
for vendorName in Vendors:
    print("cnt={0}: Vendor={1}".format(idx,vendorName))
    tile_provider = get_provider(vendorName)
    if idx==0: # make the first plot with x_range and y_range point where you want (from above)
        plot[idx] = figure(x_range=x_range, y_range=y_range,
                       x_axis_type="mercator", y_axis_type="mercator",
                       plot_height=200, plot_width=300, title=vendorName)
    
    else: # link x_range and y_range of subsequent plots to match the first
        plot[idx] = figure(x_range=plot[0].x_range, y_range=plot[0].y_range,
                       x_axis_type="mercator", y_axis_type="mercator",
                       plot_height=200, plot_width=300, title=vendorName)
    plot[idx].add_tile(tile_provider)
    idx+=1


## arrange all map views in a grid layout then add to the document
layout = layout([
    [description],
    [plot[0], plot[1], plot[2]],
    [plot[3], plot[4], plot[5]],
    [plot[6], plot[7], plot[8]],
    [plot[9]                  ]])

show(layout)