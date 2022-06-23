#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 14:15:38 2022

@author: oronald
"""

import harp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Set criteria for retrieving the data
operations = ";".join([
    "tropospheric_NO2_column_number_density_validity>75",
    "keep(latitude_bounds,longitude_bounds,tropospheric_NO2_column_number_density)",
    "bin_spatial(576, 34.203, 0.05, 675, -12.832, 0.05)",
    "derive(tropospheric_NO2_column_number_density [molec/cm2])",
    "derive(latitude {latitude})",
    "derive(longitude {longitude})"])

# Read in the file and extract the data
product = harp.import_product('/home/oronald/atm_science/no2.nc4', operations)
gridlat = np.append(product.latitude_bounds.data[:,0], product.latitude_bounds.data[-1,1])
gridlon = np.append(product.longitude_bounds.data[:,0], product.longitude_bounds.data[-1,1])

NO2val = product.tropospheric_NO2_column_number_density.data
NO2units = product.tropospheric_NO2_column_number_density.unit
NO2description = product.tropospheric_NO2_column_number_density.description


# Ste figure parameters
mpl.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16
plt.rcParams['axes.linewidth'] = 1

# Plot Figure
fig=plt.figure(figsize=(12, 8), dpi=500)
ax = plt.axes(projection=ccrs.PlateCarree())
img = plt.pcolormesh(gridlon, gridlat, NO2val[0,:,:], vmin=0, vmax=8e15, cmap='jet')
ax.coastlines(resolution='10m', color='black', linewidth=1.2)
lakes_10m = cfeature.NaturalEarthFeature('physical','lakes','10m')
ax.add_feature(cfeature.BORDERS, linewidth=1.2)
ax.add_feature(lakes_10m, facecolor='none', edgecolor='k')
cbar_kwargs = plt.gcf().add_axes([0.27, 0.05, 0.5, 0.04])
cbar = fig.colorbar(img, cbar_kwargs, ax=ax, orientation='horizontal')
cbar.set_label('$\mathregular{NO_2}$ (molecules/$\mathregular{cm^2}$)')
cbar.ax.tick_params(labelsize=16)
plt.show()