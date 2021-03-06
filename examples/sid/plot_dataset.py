"""
================================================================================
Creating and manipulating Datasets
================================================================================

**Gerd Duscher and Suhas Somnath**

08/25/2020

**This document is a simple example of how to create and manipulate Dataset
objects**

**UNDER CONSTRUCTION**
"""
# Ensure python 3 compatibility:
from __future__ import division, print_function, absolute_import, unicode_literals
import matplotlib.pylab as plt
import numpy as np
import sys

sys.path.append('../../')
import sidpy as sid


###############################################################################
print(sid.__version__)

###############################################################################
# Creating a ``sipy.Dataset`` object
# ----------------------------------
# We can create a simple sidpy Dataset from any array like object
# Here we just use a numpy array filled with zeros

data_set = sid.Dataset.from_array(np.random.random([4, 5, 10]), name='random')
print(data_set)

###############################################################################
# Note that ``data_set`` is a dask array....
# We will be improving upon the information that will be displayed when printing ``sidpy.Dataset`` objects

###############################################################################
# Accessing data within a ``Dataset``:
# Indexing of the dataset works like in numpy
# Note, that we first index and then we make a numpy array for printing reasons

print(np.array(data_set[:,0,2]))

###############################################################################
# Slicing and dicing:

###############################################################################
# Metadata
# --------
# ``sidpy`` automatically assigns generic top-level metadata regarding the
# ``Dataset``. Users are encouraged to capture the context regarding the dataset.
# The attributes included in the sidpy dataset are ``data_type``,  quantity, and  units,
# Those attributes are set to ``generic`` originally but one would want to set them t
# for the specific dataset. that will be important for plotting the data.
# Here's how one could do that:
data_set.data_type = 'spectrum_image'
data_set.units = 'nA'
data_set.quantity = 'Current'

###############################################################################
# Scientific metadata
# ~~~~~~~~~~~~~~~~~~~
# These ``Dataset`` objects can also capture rich scientific metadata such as
# acquisition parameters, etc. as well:
# We would want to add those parameters as attributes.
# These attributes could be lists, numpy arrays or simple dictionaries.
# It is encouraged to add any parameters of data analysis to the datasets,
# to keep track of input parameters. Here I made some up as an illustration:
data_set.counting =  np.arange(5)
data_set.something = {'nothing': ' ', 'value': 6.8}
data_set.acquired = 'nowhere'

print(data_set.counting)
print(data_set.something)


###############################################################################
# Another set of metadata in these Datasets is the Dimension ones:

###############################################################################
# Dimensions
# ----------
# The ``Dataset`` is automatically populated with generic information about
# each dimension of the ``Dataset``. It is a good idea to capture context
# regarding each of these dimensions using ``sidpy.Dimension``.
# As a minimum we need a name and values (of the smae length as the dimensions of the data).
# One can provide as much or as little information about each dimension.

data_set.set_dimension(0, sid.Dimension('x', np.arange(data_set.shape[0]),
                                        units='um', quantity='Length',
                                        dimension_type='spatial'))
data_set.set_dimension(1, sid.Dimension('y', np.linspace(-2, 2, num=data_set.shape[1], endpoint=True),
                                        units='um', quantity='Length',
                                        dimension_type='spatial'))
data_set.set_dimension(2, sid.Dimension('bias', np.sin(np.linspace(0, 2 * np.pi, num=data_set.shape[2])),
                                        ))
###############################################################################
# One could also manually add information regarding specific components of
# dimensions associated with Datasets via:

data_set.bias.dimension_type = 'spectral'
data_set.bias.units = 'V'
data_set.bias.quantity = 'Bias'

###############################################################################
# Let's take a look at what the dataset looks like with the additional information
# regarding the dimensions.
# Also the print function provides now a little more information about our dataset

print(data_set.bias)
print(data_set)

###############################################################################
# Plotting
# --------
# The ``Dataset`` object also comes with the ability to visualize its contents
# using the ``plot()`` function. Here we only show a simple application, but a more
# detailed description can be found in the plotting section.
# Here we plot a spectral image you can click in the image part of the plot on the
# left and the spectrum on the right will update.

data_set.plot()

###############################################################################
# The plotting depends on the data_type of the dataset and the dimension_types
# of it's dimension datasets. We set above the first two dimension_type types to
# ``spatial`` and the third one to `spectral``.
# The data_type was ``spectrum_image``.
# So the spatial dimensions are recognized as relevant for an image.
# If we change the data_type to image, we get an image.

data_set.data_type = 'image'
data_set.plot()


##########################################
# #####################################
# Saving
# ------
# These ``Dataset`` objects will be deleted from memory once the python script
# completes or when a notebook is closed. The information collected in a
# ``Dataset`` can reliably be stored to files using functions in sister
# packages - ``pyUSID`` and ``pyNSID`` that write the dataset according to the
# **Universal Spectroscopy and Imaging Data (USID)** or **N-dimensional
# Spectrocsopy and Imaging Data (NSID)** formats.
# Here are links to how one could save such Datasets for each package:


