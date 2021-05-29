
.. image:: https://raw.githubusercontent.com/corriporai/runpandas/master/docs/source/_static/images/runpandas_banner.png

RunPandas - Python Package for handing running data from GPS-enabled tracking devices and applications.
=======================================================================================================

.. image:: https://img.shields.io/pypi/v/runpandas.svg
    :target: https://pypi.python.org/pypi/runpandas/

.. image:: https://anaconda.org/marcelcaraciolo/runpandas/badges/version.svg
    :target: https://anaconda.org/marcelcaraciolo/runpandas


.. image:: https://www.codefactor.io/repository/github/corriporai/runpandas/badge
   :target: https://www.codefactor.io/repository/github/corriporai/runpandas
   :alt: CodeFactor

.. image:: https://github.com/corriporai/runpandas/workflows/Build/badge.svg?branch=master
    :target: https://github.com/corriporai/runpandas/actions/workflows/build.yml

.. image:: https://coveralls.io/repos/github/corriporai/runpandas/badge.svg?branch=master
    :target: https://coveralls.io/github/corriporai/runpandas

.. image:: https://codecov.io/gh/corriporai/runpandas/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/corriporai/runpandas

.. image:: https://readthedocs.org/projects/runpandas/badge/?version=latest
    :target: https://runpandas.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/psf/black

.. image:: https://static.pepy.tech/personalized-badge/runpandas?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads
   :target: https://pepy.tech/project/runpandas

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/corriporai/runpandas/HEAD
 
.. image:: https://zenodo.org/badge/272209151.svg
   :target: https://zenodo.org/badge/latestdoi/272209151

=========

Introduction
------------

RunPandas is a project to add support for data collected by GPS-enabled tracking devices,
heart rate monitors data to  [pandas](http://pandas.pydata.org) objects.
It is a Python package that provides infrastructure for importing tracking data
from such devices, enabling statistical and visual analysis for running enthusiasts and lovers.
Its goal is to fill the gap between the routine collection of data and their manual analyses in Pandas and Python.

Documentation
-------------
`Stable documentation `__
is available on
`github.io <https://corriporai.github.io/runpandas/>`__.
A second copy of the stable documentation is hosted on
`read the docs <https://runpandas.readthedocs.io/>`_ for more details.

`Development documentation <https://corriporai.github.io/runpandas/devel/>`__
is available for the latest changes in master.

==> Check out `this Blog post <https://corriporai.github.io/pandasrunner/general/2020/08/01/welcome-to-runpandas.html>`_
for the reasoning and philosophy behind Runpandas, as well as a detailed tutorial with code examples.

==> Follow `this Runpandas live book <https://github.com/corriporai/runpandasbook>`_ in Jupyter notebook format based on `Jupyter Books <https://jupyterbook.org/intro.html>`_.


Install
--------

 RunPandas depends on the following packages:

- ``pandas``
- ``fitparse``
- ``stravalib``
- ``pydantic``
- ``pyaml``
- ``haversine``

Runpandas was tested to work on \*nix-like systems, including macOS.

-----

Install latest release version via pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   $ pip install runpandas

Install latest release version via conda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   $ conda install -c marcelcaraciolo runpandas


Install latest development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ pip install git+https://github.com/corriporai/runpandas.git

or

.. code-block:: shell

    $ git clone https://github.com/corriporai/runpandas.git
    $ python setup.py install


Examples
--------


Install using ``pip`` and then import and use one of the tracking
readers. This example loads a local file.tcx. From the data file, we
obviously get time, altitude, distance, heart rate and geo position
(lat/long).

.. code:: ipython3

    # !pip install runpandas
    import runpandas as rpd
    activity = rpd.read_file('./sample.tcx')

.. code:: ipython3

    activity.head(5)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>alt</th>
          <th>dist</th>
          <th>hr</th>
          <th>lon</th>
          <th>lat</th>
        </tr>
        <tr>
          <th>time</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>00:00:00</th>
          <td>178.942627</td>
          <td>0.000000</td>
          <td>62.0</td>
          <td>-79.093187</td>
          <td>35.951880</td>
        </tr>
        <tr>
          <th>00:00:01</th>
          <td>178.942627</td>
          <td>0.000000</td>
          <td>62.0</td>
          <td>-79.093184</td>
          <td>35.951880</td>
        </tr>
        <tr>
          <th>00:00:06</th>
          <td>178.942627</td>
          <td>1.106947</td>
          <td>62.0</td>
          <td>-79.093172</td>
          <td>35.951868</td>
        </tr>
        <tr>
          <th>00:00:12</th>
          <td>177.500610</td>
          <td>13.003035</td>
          <td>62.0</td>
          <td>-79.093228</td>
          <td>35.951774</td>
        </tr>
        <tr>
          <th>00:00:16</th>
          <td>177.500610</td>
          <td>22.405027</td>
          <td>60.0</td>
          <td>-79.093141</td>
          <td>35.951732</td>
        </tr>
      </tbody>
    </table>
    </div>



The data frames that are returned by runpandas when loading files is
similar for different file types. The dataframe in the above example is
a subclass of the ``pandas.DataFrame`` and provides some additional
features. Certain columns also return specific ``pandas.Series``
subclasses, which provides useful methods:

.. code:: ipython3

    print (type(activity))
    print(type(activity.alt))


.. parsed-literal::

    <class 'runpandas.types.frame.Activity'>
    <class 'runpandas.types.columns.Altitude'>


For instance, if you want to get the base unit for the altitude ``alt``
data or the distance ``dist`` data:

.. code:: ipython3

    print(activity.alt.base_unit)
    print(activity.alt.sum())


.. parsed-literal::

    m
    65883.68151855901


.. code:: ipython3

    print(activity.dist.base_unit)
    print(activity.dist[-1])


.. parsed-literal::

    m
    4686.31103516


The ``Activity`` dataframe also contains special properties that
presents some statistics from the workout such as elapsed time, mean
heartrate, the moving time and the distance of workout in meters.

.. code:: ipython3

    #total time elapsed for the activity
    print(activity.ellapsed_time)
    #distance of workout in meters
    print(activity.distance)
    #mean heartrate
    print(activity.mean_heart_rate())


.. parsed-literal::

    0 days 00:33:11
    4686.31103516
    156.65274151436032


Occasionally, some observations such as speed, distance and others must
be calculated based on available data in the given activity. In
runpandas there are special accessors (``runpandas.acessors``) that
computes some of these metrics. We will compute the ``speed`` and the
``distance per position`` observations using the latitude and longitude
for each record and calculate the haversine distance in meters and the
speed in meters per second.

.. code:: ipython3

    #compute the distance using haversine formula between two consecutive latitude, longitudes observations.
    activity['distpos']  = activity.compute.distance()
    activity['distpos'].head()




.. parsed-literal::

    time
    00:00:00          NaN
    00:00:01     0.333146
    00:00:06     1.678792
    00:00:12    11.639901
    00:00:16     9.183847
    Name: distpos, dtype: float64



.. code:: ipython3

    #compute the distance using haversine formula between two consecutive latitude, longitudes observations.
    activity['speed']  = activity.compute.speed(from_distances=True)
    activity['speed'].head()




.. parsed-literal::

    time
    00:00:00         NaN
    00:00:01    0.333146
    00:00:06    0.335758
    00:00:12    1.939984
    00:00:16    2.295962
    Name: speed, dtype: float64


Popular running metrics are also available through the runpandas
acessors such as gradient, pace, vertical speed , etc.

.. code:: ipython3

    activity['vam'] = activity.compute.vertical_speed()
    activity['vam'].head()




.. parsed-literal::

    time
    00:00:00         NaN
    00:00:01    0.000000
    00:00:06    0.000000
    00:00:12   -0.240336
    00:00:16    0.000000
    Name: vam, dtype: float64


Sporadically, there will be a large time difference between consecutive
observations in the same workout. This can happen when device is paused
by the athlete or therere proprietary algorithms controlling the
operating sampling rate of the device which can auto-pause when the
device detects no significant change in position. In runpandas there is
an algorithm that will attempt to calculate the moving time based on the
GPS locations, distances, and speed of the activity.

To compute the moving time, there is a special acessor that detects the
periods of inactivity and returns the ``moving`` series containing all
the observations considered to be stopped.

.. code:: ipython3

    activity_only_moving = activity.only_moving()
    print(activity_only_moving['moving'].head())


.. parsed-literal::

    time
    00:00:00    False
    00:00:01    False
    00:00:06    False
    00:00:12     True
    00:00:16     True
    Name: moving, dtype: bool


Now we can compute the moving time, the time of how long the user were
active.

.. code:: ipython3

    activity_only_moving.moving_time




.. parsed-literal::

    Timedelta('0 days 00:33:05')



Now, let’s play with the data. Let’s show distance vs as an example of
what and how we can create visualizations. In this example, we will use
the built in, matplotlib based plot function.

.. code:: ipython3

    activity[['dist']].plot()


.. parsed-literal::

    Matplotlib is building the font cache; this may take a moment.




.. parsed-literal::

    <AxesSubplot:xlabel='time'>




.. image:: examples/overview_files/overview_10_2.svg


And here is altitude versus time.

.. code:: ipython3

    activity[['alt']].plot()




.. parsed-literal::

    <AxesSubplot:xlabel='time'>




.. image:: examples/overview_files/overview_12_1.svg


Finally, lest’s show the altitude vs distance profile. Here is a
scatterplot that shows altitude vs distance as recorded.

.. code:: ipython3

    activity.plot.scatter(x='dist', y='alt', c='DarkBlue')




.. parsed-literal::

    <AxesSubplot:xlabel='dist', ylabel='alt'>




.. image:: examples/overview_files/overview_14_1.svg


Finally, let’s watch a glimpse of the map route by plotting a 2d map
using logintude vs latitude.

.. code:: ipython3

    activity.plot(x='lon', y='lat')




.. parsed-literal::

    <AxesSubplot:xlabel='lon'>




.. image:: examples/overview_files/overview_16_1.svg


The ``runpandas`` package also comes with extra batteries, such as our
``runpandas.datasets`` package, which includes a range of example data
for testing purposes. There is a dedicated
`repository <https://github.com/corriporai/runpandas-data>`__ with all
the data available. An index of the data is kept
`here <https://github.com/corriporai/runpandas-data/blob/master/activities/index.yml>`__.

You can use the example data available:

.. code:: ipython3

    example_fit = rpd.activity_examples(path='Garmin_Fenix_6S_Pro-Running.fit')
    print(example_fit.summary)
    print('Included metrics:', example_fit.included_data)


.. parsed-literal::

    Synced from watch Garmin Fenix 6S
    
    Included metrics: [<MetricsEnum.latitude: 'latitude'>, <MetricsEnum.longitude: 'longitude'>, <MetricsEnum.elevation: 'elevation'>, <MetricsEnum.heartrate: 'heartrate'>, <MetricsEnum.cadence: 'cadence'>, <MetricsEnum.distance: 'distance'>, <MetricsEnum.temperature: 'temperature'>]


.. code:: ipython3

    rpd.read_file(example_fit.path).head()


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>enhanced_speed</th>
          <th>enhanced_altitude</th>
          <th>unknown_87</th>
          <th>fractional_cadence</th>
          <th>lap</th>
          <th>session</th>
          <th>unknown_108</th>
          <th>dist</th>
          <th>cad</th>
          <th>hr</th>
          <th>lon</th>
          <th>lat</th>
          <th>temp</th>
        </tr>
        <tr>
          <th>time</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>00:00:00</th>
          <td>0.000</td>
          <td>254.0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
          <td>0.00</td>
          <td>0</td>
          <td>101</td>
          <td>13.843376</td>
          <td>51.066280</td>
          <td>8</td>
        </tr>
        <tr>
          <th>00:00:01</th>
          <td>0.000</td>
          <td>254.0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
          <td>0.00</td>
          <td>0</td>
          <td>101</td>
          <td>13.843374</td>
          <td>51.066274</td>
          <td>8</td>
        </tr>
        <tr>
          <th>00:00:10</th>
          <td>1.698</td>
          <td>254.0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0</td>
          <td>1</td>
          <td>2362.0</td>
          <td>0.00</td>
          <td>83</td>
          <td>97</td>
          <td>13.843176</td>
          <td>51.066249</td>
          <td>8</td>
        </tr>
        <tr>
          <th>00:00:12</th>
          <td>2.267</td>
          <td>254.0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0</td>
          <td>1</td>
          <td>2362.0</td>
          <td>3.95</td>
          <td>84</td>
          <td>99</td>
          <td>13.843118</td>
          <td>51.066250</td>
          <td>8</td>
        </tr>
        <tr>
          <th>00:00:21</th>
          <td>2.127</td>
          <td>254.6</td>
          <td>0</td>
          <td>0.5</td>
          <td>0</td>
          <td>1</td>
          <td>2552.0</td>
          <td>16.67</td>
          <td>87</td>
          <td>100</td>
          <td>13.842940</td>
          <td>51.066231</td>
          <td>8</td>
        </tr>
      </tbody>
    </table>
    </div>



In case of you just only want to see all the activities in a specific
file type , you can filter the ``runpandas.activities_examples``, which
returns a filter iterable that you can iterate over:

.. code:: ipython3

    fit_examples = rpd.activity_examples(file_type=rpd.FileTypeEnum.FIT)
    for example in fit_examples:
        #Download and play with the filtered examples
        print(example.path)


.. parsed-literal::

    https://raw.githubusercontent.com/corriporai/runpandas-data/master/activities/Garmin_Fenix_6S_Pro-Running.fit
    https://raw.githubusercontent.com/corriporai/runpandas-data/master/activities/Garmin_Fenix2_running_with_hrm.fit
    https://raw.githubusercontent.com/corriporai/runpandas-data/master/activities/Garmin_Forerunner_910XT-Running.fit



Get in touch
------------
- Report bugs, suggest features or view the source code [on GitHub](https://github.com/corriporai/runpandas).

I'm very interested in your experience with runpandas.
Please drop me an note with any feedback you have.

Contributions welcome!

\- **Marcel Caraciolo**

License
-------
Runpandas is licensed under the **MIT License**. A copy of which is included in LICENSE.
