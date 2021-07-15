.. code:: ipython3

    %load_ext autoreload
    %autoreload 2

Quick Start
===========

Install using ``pip`` and then import and use one of the tracking
readers. This example loads a local file.tcx. From the data file, we
obviously get time, altitude, distance, heart rate and geo position
(lat/long).

.. code:: ipython3

    import warnings
    warnings.filterwarnings('ignore')

.. code:: ipython3

    #!pip install runpandas
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
          <td>62</td>
          <td>-79.093187</td>
          <td>35.951880</td>
        </tr>
        <tr>
          <th>00:00:01</th>
          <td>178.942627</td>
          <td>0.000000</td>
          <td>62</td>
          <td>-79.093184</td>
          <td>35.951880</td>
        </tr>
        <tr>
          <th>00:00:06</th>
          <td>178.942627</td>
          <td>1.106947</td>
          <td>62</td>
          <td>-79.093172</td>
          <td>35.951868</td>
        </tr>
        <tr>
          <th>00:00:12</th>
          <td>177.500610</td>
          <td>13.003035</td>
          <td>62</td>
          <td>-79.093228</td>
          <td>35.951774</td>
        </tr>
        <tr>
          <th>00:00:16</th>
          <td>177.500610</td>
          <td>22.405027</td>
          <td>60</td>
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



Runpandas also provides a method ``summary`` for summarising the
activity through common statistics. Such a session summary includes
estimates of several metrics computed above with a single call.

.. code:: ipython3

    activity_only_moving.summary()




.. parsed-literal::

    Session                           Running: 26-12-2012 21:29:53
    Total distance (meters)                                4686.31
    Total ellapsed time                            0 days 00:33:11
    Total moving time                              0 days 00:33:05
    Average speed (km/h)                                   8.47656
    Average moving speed (km/h)                            8.49853
    Average pace (per 1 km)                        0 days 00:07:04
    Average pace moving (per 1 km)                 0 days 00:07:03
    Average cadence                                            NaN
    Average moving cadence                                     NaN
    Average heart rate                                     156.653
    Average moving heart rate                                157.4
    Average temperature                                        NaN
    dtype: object



Now, let’s play with the data. Let’s show distance vs as an example of
what and how we can create visualizations. In this example, we will use
the built in, matplotlib based plot function.

.. code:: ipython3

    activity[['dist']].plot()




.. parsed-literal::

    <AxesSubplot:xlabel='time'>




.. image:: overview_files/overview_24_1.svg


And here is altitude versus time.

.. code:: ipython3

    activity[['alt']].plot()




.. parsed-literal::

    <AxesSubplot:xlabel='time'>




.. image:: overview_files/overview_26_1.svg


Finally, lest’s show the altitude vs distance profile. Here is a
scatterplot that shows altitude vs distance as recorded.

.. code:: ipython3

    activity.plot.scatter(x='dist', y='alt', c='DarkBlue')




.. parsed-literal::

    <AxesSubplot:xlabel='dist', ylabel='alt'>




.. image:: overview_files/overview_28_1.svg


Finally, let’s watch a glimpse of the map route by plotting a 2d map
using logintude vs latitude.

.. code:: ipython3

    activity.plot(x='lon', y='lat')




.. parsed-literal::

    <AxesSubplot:xlabel='lon'>




.. image:: overview_files/overview_30_1.svg


Ok, a 2D map is cool. But would it be possible plot the route above on
Google Maps ? For this task, we will use a ready-made package called
`gmplot <https://github.com/gmplot/gmplot>`__. It uses the Google Maps
API together with its Python library.

.. code:: ipython3

    import gmplot
    
    #let's get the min/max latitude and longitudes
    min_lat, max_lat, min_lon, max_lon = \
    min(activity['lat']), max(activity['lat']), \
    min(activity['lon']), max(activity['lon'])
    
    ## Create empty map with zoom level 16
    mymap = gmplot.GoogleMapPlotter(
        min_lat + (max_lat - min_lat) / 2, 
        min_lon + (max_lon - min_lon) / 2, 
        16, apikey='YOUR API KEY')
    #To plot the data as a continuous line (or a polygon), we can use the plot method. It has two self-explanatory optional arguments: color and edge width.
    mymap.plot(activity['lat'], activity['lon'], 'blue', edge_width=1)
    
    #Draw the map to an HTML file.
    mymap.draw('myroute.html')

.. code:: ipython3

    #Show the map!
    import IPython
    IPython.display.HTML(filename='myroute.html')




.. raw:: html

    <html>
    <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>Google Maps - gmplot</title>
    <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&key=YOUR API KEY"></script>
    <script type="text/javascript">
        function initialize() {
            var map = new google.maps.Map(document.getElementById("map_canvas"), {
                zoom: 16,
                center: new google.maps.LatLng(35.949324, -79.094538)
            });
    
            new google.maps.Polyline({
                clickable: false,
                geodesic: true,
                strokeColor: "#0000FF",
                strokeOpacity: 1.000000,
                strokeWeight: 1,
                map: map,
                path: [
                    new google.maps.LatLng(35.951880, -79.093187),
                    new google.maps.LatLng(35.951880, -79.093184),
                    new google.maps.LatLng(35.951868, -79.093172),
                    new google.maps.LatLng(35.951774, -79.093228),
                    new google.maps.LatLng(35.951732, -79.093141),
                    new google.maps.LatLng(35.951644, -79.093049),
                    new google.maps.LatLng(35.951579, -79.093025),
                    new google.maps.LatLng(35.951494, -79.093017),
                    new google.maps.LatLng(35.951481, -79.093016),
                    new google.maps.LatLng(35.951419, -79.093030),
                    new google.maps.LatLng(35.951352, -79.093080),
                    new google.maps.LatLng(35.951274, -79.093121),
                    new google.maps.LatLng(35.951198, -79.093166),
                    new google.maps.LatLng(35.951157, -79.093187),
                    new google.maps.LatLng(35.951088, -79.093244),
                    new google.maps.LatLng(35.951105, -79.093323),
                    new google.maps.LatLng(35.951216, -79.093485),
                    new google.maps.LatLng(35.951274, -79.093617),
                    new google.maps.LatLng(35.951331, -79.093818),
                    new google.maps.LatLng(35.951333, -79.093848),
                    new google.maps.LatLng(35.951335, -79.093876),
                    new google.maps.LatLng(35.951339, -79.093905),
                    new google.maps.LatLng(35.951345, -79.094048),
                    new google.maps.LatLng(35.951331, -79.094189),
                    new google.maps.LatLng(35.951277, -79.094358),
                    new google.maps.LatLng(35.951256, -79.094492),
                    new google.maps.LatLng(35.951260, -79.094588),
                    new google.maps.LatLng(35.951193, -79.094823),
                    new google.maps.LatLng(35.951086, -79.094987),
                    new google.maps.LatLng(35.951019, -79.095058),
                    new google.maps.LatLng(35.950899, -79.095169),
                    new google.maps.LatLng(35.950789, -79.095241),
                    new google.maps.LatLng(35.950657, -79.095301),
                    new google.maps.LatLng(35.950612, -79.095313),
                    new google.maps.LatLng(35.950590, -79.095322),
                    new google.maps.LatLng(35.950477, -79.095344),
                    new google.maps.LatLng(35.950358, -79.095351),
                    new google.maps.LatLng(35.950228, -79.095336),
                    new google.maps.LatLng(35.950180, -79.095338),
                    new google.maps.LatLng(35.950061, -79.095341),
                    new google.maps.LatLng(35.949987, -79.095339),
                    new google.maps.LatLng(35.949909, -79.095339),
                    new google.maps.LatLng(35.949889, -79.095340),
                    new google.maps.LatLng(35.949776, -79.095345),
                    new google.maps.LatLng(35.949673, -79.095347),
                    new google.maps.LatLng(35.949536, -79.095355),
                    new google.maps.LatLng(35.949392, -79.095373),
                    new google.maps.LatLng(35.949347, -79.095481),
                    new google.maps.LatLng(35.949347, -79.095508),
                    new google.maps.LatLng(35.949339, -79.095676),
                    new google.maps.LatLng(35.949337, -79.095824),
                    new google.maps.LatLng(35.949344, -79.095956),
                    new google.maps.LatLng(35.949346, -79.096094),
                    new google.maps.LatLng(35.949345, -79.096249),
                    new google.maps.LatLng(35.949350, -79.096333),
                    new google.maps.LatLng(35.949351, -79.096362),
                    new google.maps.LatLng(35.949351, -79.096416),
                    new google.maps.LatLng(35.949351, -79.096442),
                    new google.maps.LatLng(35.949348, -79.096465),
                    new google.maps.LatLng(35.949345, -79.096548),
                    new google.maps.LatLng(35.949345, -79.096577),
                    new google.maps.LatLng(35.949343, -79.096810),
                    new google.maps.LatLng(35.949345, -79.096995),
                    new google.maps.LatLng(35.949299, -79.097163),
                    new google.maps.LatLng(35.949282, -79.097181),
                    new google.maps.LatLng(35.949176, -79.097171),
                    new google.maps.LatLng(35.949087, -79.097136),
                    new google.maps.LatLng(35.948975, -79.097074),
                    new google.maps.LatLng(35.948828, -79.097008),
                    new google.maps.LatLng(35.948809, -79.097006),
                    new google.maps.LatLng(35.948708, -79.096976),
                    new google.maps.LatLng(35.948660, -79.096963),
                    new google.maps.LatLng(35.948635, -79.096957),
                    new google.maps.LatLng(35.948480, -79.096929),
                    new google.maps.LatLng(35.948433, -79.096923),
                    new google.maps.LatLng(35.948333, -79.096928),
                    new google.maps.LatLng(35.948205, -79.096917),
                    new google.maps.LatLng(35.948154, -79.096814),
                    new google.maps.LatLng(35.948142, -79.096677),
                    new google.maps.LatLng(35.948143, -79.096566),
                    new google.maps.LatLng(35.948138, -79.096457),
                    new google.maps.LatLng(35.948120, -79.096322),
                    new google.maps.LatLng(35.948120, -79.096180),
                    new google.maps.LatLng(35.948106, -79.096006),
                    new google.maps.LatLng(35.948110, -79.095893),
                    new google.maps.LatLng(35.948105, -79.095804),
                    new google.maps.LatLng(35.948094, -79.095637),
                    new google.maps.LatLng(35.948090, -79.095499),
                    new google.maps.LatLng(35.948090, -79.095353),
                    new google.maps.LatLng(35.948072, -79.095169),
                    new google.maps.LatLng(35.948058, -79.095005),
                    new google.maps.LatLng(35.948043, -79.094829),
                    new google.maps.LatLng(35.948041, -79.094667),
                    new google.maps.LatLng(35.948053, -79.094502),
                    new google.maps.LatLng(35.948061, -79.094324),
                    new google.maps.LatLng(35.948099, -79.094209),
                    new google.maps.LatLng(35.948142, -79.094066),
                    new google.maps.LatLng(35.948185, -79.093944),
                    new google.maps.LatLng(35.948246, -79.093811),
                    new google.maps.LatLng(35.948319, -79.093658),
                    new google.maps.LatLng(35.948396, -79.093540),
                    new google.maps.LatLng(35.948500, -79.093413),
                    new google.maps.LatLng(35.948613, -79.093303),
                    new google.maps.LatLng(35.948738, -79.093194),
                    new google.maps.LatLng(35.948856, -79.093095),
                    new google.maps.LatLng(35.948988, -79.092973),
                    new google.maps.LatLng(35.949107, -79.092860),
                    new google.maps.LatLng(35.949237, -79.092740),
                    new google.maps.LatLng(35.949434, -79.092566),
                    new google.maps.LatLng(35.949619, -79.092395),
                    new google.maps.LatLng(35.949742, -79.092286),
                    new google.maps.LatLng(35.949971, -79.092070),
                    new google.maps.LatLng(35.950035, -79.092006),
                    new google.maps.LatLng(35.950144, -79.091944),
                    new google.maps.LatLng(35.950314, -79.091908),
                    new google.maps.LatLng(35.950345, -79.091906),
                    new google.maps.LatLng(35.950578, -79.091974),
                    new google.maps.LatLng(35.950722, -79.092121),
                    new google.maps.LatLng(35.950823, -79.092312),
                    new google.maps.LatLng(35.950914, -79.092521),
                    new google.maps.LatLng(35.951033, -79.092802),
                    new google.maps.LatLng(35.951091, -79.092971),
                    new google.maps.LatLng(35.951184, -79.093208),
                    new google.maps.LatLng(35.951248, -79.093378),
                    new google.maps.LatLng(35.951312, -79.093529),
                    new google.maps.LatLng(35.951361, -79.093665),
                    new google.maps.LatLng(35.951388, -79.093839),
                    new google.maps.LatLng(35.951409, -79.094036),
                    new google.maps.LatLng(35.951390, -79.094263),
                    new google.maps.LatLng(35.951366, -79.094398),
                    new google.maps.LatLng(35.951349, -79.094496),
                    new google.maps.LatLng(35.951313, -79.094620),
                    new google.maps.LatLng(35.951301, -79.094675),
                    new google.maps.LatLng(35.951202, -79.094820),
                    new google.maps.LatLng(35.951131, -79.094915),
                    new google.maps.LatLng(35.951083, -79.094967),
                    new google.maps.LatLng(35.950977, -79.095078),
                    new google.maps.LatLng(35.950887, -79.095149),
                    new google.maps.LatLng(35.950780, -79.095203),
                    new google.maps.LatLng(35.950688, -79.095230),
                    new google.maps.LatLng(35.950554, -79.095269),
                    new google.maps.LatLng(35.950415, -79.095280),
                    new google.maps.LatLng(35.950292, -79.095272),
                    new google.maps.LatLng(35.950153, -79.095266),
                    new google.maps.LatLng(35.950042, -79.095265),
                    new google.maps.LatLng(35.950021, -79.095264),
                    new google.maps.LatLng(35.949894, -79.095274),
                    new google.maps.LatLng(35.949795, -79.095271),
                    new google.maps.LatLng(35.949693, -79.095278),
                    new google.maps.LatLng(35.949578, -79.095289),
                    new google.maps.LatLng(35.949503, -79.095292),
                    new google.maps.LatLng(35.949403, -79.095368),
                    new google.maps.LatLng(35.949397, -79.095467),
                    new google.maps.LatLng(35.949385, -79.095600),
                    new google.maps.LatLng(35.949378, -79.095743),
                    new google.maps.LatLng(35.949366, -79.095924),
                    new google.maps.LatLng(35.949368, -79.096141),
                    new google.maps.LatLng(35.949371, -79.096340),
                    new google.maps.LatLng(35.949362, -79.096523),
                    new google.maps.LatLng(35.949358, -79.096700),
                    new google.maps.LatLng(35.949358, -79.096907),
                    new google.maps.LatLng(35.949315, -79.097097),
                    new google.maps.LatLng(35.949296, -79.097125),
                    new google.maps.LatLng(35.949184, -79.097123),
                    new google.maps.LatLng(35.949141, -79.097106),
                    new google.maps.LatLng(35.949036, -79.097067),
                    new google.maps.LatLng(35.948916, -79.097033),
                    new google.maps.LatLng(35.948792, -79.097003),
                    new google.maps.LatLng(35.948693, -79.096977),
                    new google.maps.LatLng(35.948567, -79.096950),
                    new google.maps.LatLng(35.948416, -79.096934),
                    new google.maps.LatLng(35.948286, -79.096917),
                    new google.maps.LatLng(35.948194, -79.096907),
                    new google.maps.LatLng(35.948137, -79.096775),
                    new google.maps.LatLng(35.948134, -79.096749),
                    new google.maps.LatLng(35.948127, -79.096577),
                    new google.maps.LatLng(35.948112, -79.096440),
                    new google.maps.LatLng(35.948101, -79.096318),
                    new google.maps.LatLng(35.948092, -79.096177),
                    new google.maps.LatLng(35.948094, -79.096023),
                    new google.maps.LatLng(35.948088, -79.095921),
                    new google.maps.LatLng(35.948078, -79.095761),
                    new google.maps.LatLng(35.948068, -79.095643),
                    new google.maps.LatLng(35.948067, -79.095509),
                    new google.maps.LatLng(35.948061, -79.095352),
                    new google.maps.LatLng(35.948061, -79.095330),
                    new google.maps.LatLng(35.948060, -79.095262),
                    new google.maps.LatLng(35.948054, -79.095134),
                    new google.maps.LatLng(35.948050, -79.094999),
                    new google.maps.LatLng(35.948042, -79.094866),
                    new google.maps.LatLng(35.948046, -79.094712),
                    new google.maps.LatLng(35.948043, -79.094578),
                    new google.maps.LatLng(35.948045, -79.094345),
                    new google.maps.LatLng(35.948053, -79.094272),
                    new google.maps.LatLng(35.948097, -79.094161),
                    new google.maps.LatLng(35.948116, -79.094079),
                    new google.maps.LatLng(35.948175, -79.093930),
                    new google.maps.LatLng(35.948233, -79.093785),
                    new google.maps.LatLng(35.948288, -79.093654),
                    new google.maps.LatLng(35.948330, -79.093595),
                    new google.maps.LatLng(35.948413, -79.093483),
                    new google.maps.LatLng(35.948504, -79.093362),
                    new google.maps.LatLng(35.948597, -79.093267),
                    new google.maps.LatLng(35.948711, -79.093168),
                    new google.maps.LatLng(35.948814, -79.093083),
                    new google.maps.LatLng(35.948889, -79.093016),
                    new google.maps.LatLng(35.948974, -79.092941),
                    new google.maps.LatLng(35.949072, -79.092853),
                    new google.maps.LatLng(35.949185, -79.092750),
                    new google.maps.LatLng(35.949334, -79.092620),
                    new google.maps.LatLng(35.949497, -79.092474),
                    new google.maps.LatLng(35.949590, -79.092393),
                    new google.maps.LatLng(35.949685, -79.092311),
                    new google.maps.LatLng(35.949795, -79.092219),
                    new google.maps.LatLng(35.949910, -79.092119),
                    new google.maps.LatLng(35.950018, -79.092024),
                    new google.maps.LatLng(35.950122, -79.091951),
                    new google.maps.LatLng(35.950236, -79.091911),
                    new google.maps.LatLng(35.950349, -79.091895),
                    new google.maps.LatLng(35.950464, -79.091915),
                    new google.maps.LatLng(35.950535, -79.091945),
                    new google.maps.LatLng(35.950657, -79.092024),
                    new google.maps.LatLng(35.950750, -79.092130),
                    new google.maps.LatLng(35.950829, -79.092278),
                    new google.maps.LatLng(35.950872, -79.092382),
                    new google.maps.LatLng(35.950917, -79.092511),
                    new google.maps.LatLng(35.950970, -79.092634),
                    new google.maps.LatLng(35.951016, -79.092740),
                    new google.maps.LatLng(35.951058, -79.092826),
                    new google.maps.LatLng(35.951108, -79.092958),
                    new google.maps.LatLng(35.951164, -79.093075),
                    new google.maps.LatLng(35.951213, -79.093209),
                    new google.maps.LatLng(35.951260, -79.093341),
                    new google.maps.LatLng(35.951341, -79.093535),
                    new google.maps.LatLng(35.951374, -79.093706),
                    new google.maps.LatLng(35.951392, -79.093861),
                    new google.maps.LatLng(35.951404, -79.093998),
                    new google.maps.LatLng(35.951390, -79.094215),
                    new google.maps.LatLng(35.951343, -79.094425),
                    new google.maps.LatLng(35.951286, -79.094609),
                    new google.maps.LatLng(35.951236, -79.094687),
                    new google.maps.LatLng(35.951153, -79.094796),
                    new google.maps.LatLng(35.951066, -79.094894),
                    new google.maps.LatLng(35.950969, -79.094990),
                    new google.maps.LatLng(35.950876, -79.095054),
                    new google.maps.LatLng(35.950796, -79.095108),
                    new google.maps.LatLng(35.950689, -79.095152),
                    new google.maps.LatLng(35.950593, -79.095174),
                    new google.maps.LatLng(35.950493, -79.095196),
                    new google.maps.LatLng(35.950415, -79.095209),
                    new google.maps.LatLng(35.950325, -79.095212),
                    new google.maps.LatLng(35.950213, -79.095206),
                    new google.maps.LatLng(35.950143, -79.095207),
                    new google.maps.LatLng(35.950046, -79.095210),
                    new google.maps.LatLng(35.949979, -79.095219),
                    new google.maps.LatLng(35.949883, -79.095228),
                    new google.maps.LatLng(35.949791, -79.095223),
                    new google.maps.LatLng(35.949726, -79.095239),
                    new google.maps.LatLng(35.949694, -79.095238),
                    new google.maps.LatLng(35.949651, -79.095237),
                    new google.maps.LatLng(35.949517, -79.095244),
                    new google.maps.LatLng(35.949394, -79.095259),
                    new google.maps.LatLng(35.949359, -79.095351),
                    new google.maps.LatLng(35.949354, -79.095507),
                    new google.maps.LatLng(35.949355, -79.095623),
                    new google.maps.LatLng(35.949351, -79.095766),
                    new google.maps.LatLng(35.949347, -79.095885),
                    new google.maps.LatLng(35.949351, -79.096022),
                    new google.maps.LatLng(35.949348, -79.096170),
                    new google.maps.LatLng(35.949351, -79.096358),
                    new google.maps.LatLng(35.949348, -79.096494),
                    new google.maps.LatLng(35.949342, -79.096561),
                    new google.maps.LatLng(35.949343, -79.096758),
                    new google.maps.LatLng(35.949321, -79.096953),
                    new google.maps.LatLng(35.949308, -79.097004),
                    new google.maps.LatLng(35.949233, -79.097090),
                    new google.maps.LatLng(35.949130, -79.097057),
                    new google.maps.LatLng(35.949023, -79.097016),
                    new google.maps.LatLng(35.948911, -79.096977),
                    new google.maps.LatLng(35.948815, -79.096948),
                    new google.maps.LatLng(35.948722, -79.096932),
                    new google.maps.LatLng(35.948591, -79.096906),
                    new google.maps.LatLng(35.948502, -79.096887),
                    new google.maps.LatLng(35.948400, -79.096870),
                    new google.maps.LatLng(35.948284, -79.096865),
                    new google.maps.LatLng(35.948265, -79.096864),
                    new google.maps.LatLng(35.948245, -79.096864),
                    new google.maps.LatLng(35.948202, -79.096858),
                    new google.maps.LatLng(35.948057, -79.096847),
                    new google.maps.LatLng(35.947932, -79.096846),
                    new google.maps.LatLng(35.947809, -79.096841),
                    new google.maps.LatLng(35.947719, -79.096842),
                    new google.maps.LatLng(35.947653, -79.096834),
                    new google.maps.LatLng(35.947568, -79.096835),
                    new google.maps.LatLng(35.947523, -79.096834),
                    new google.maps.LatLng(35.947445, -79.096826),
                    new google.maps.LatLng(35.947384, -79.096824),
                    new google.maps.LatLng(35.947368, -79.096823),
                    new google.maps.LatLng(35.947333, -79.096818),
                    new google.maps.LatLng(35.947238, -79.096799),
                    new google.maps.LatLng(35.947158, -79.096796),
                    new google.maps.LatLng(35.947143, -79.096796),
                    new google.maps.LatLng(35.947017, -79.096792),
                    new google.maps.LatLng(35.946929, -79.096792),
                    new google.maps.LatLng(35.946847, -79.096785),
                    new google.maps.LatLng(35.946694, -79.096796),
                    new google.maps.LatLng(35.946733, -79.096798),
                    new google.maps.LatLng(35.946845, -79.096794),
                    new google.maps.LatLng(35.946961, -79.096796),
                    new google.maps.LatLng(35.947093, -79.096808),
                    new google.maps.LatLng(35.947198, -79.096811),
                    new google.maps.LatLng(35.947341, -79.096822),
                    new google.maps.LatLng(35.947467, -79.096834),
                    new google.maps.LatLng(35.947592, -79.096837),
                    new google.maps.LatLng(35.947717, -79.096841),
                    new google.maps.LatLng(35.947916, -79.096850),
                    new google.maps.LatLng(35.948050, -79.096837),
                    new google.maps.LatLng(35.948097, -79.096791),
                    new google.maps.LatLng(35.948094, -79.096595),
                    new google.maps.LatLng(35.948089, -79.096471),
                    new google.maps.LatLng(35.948090, -79.096394),
                    new google.maps.LatLng(35.948091, -79.096284),
                    new google.maps.LatLng(35.948091, -79.096169),
                    new google.maps.LatLng(35.948089, -79.096083),
                    new google.maps.LatLng(35.948076, -79.095999),
                    new google.maps.LatLng(35.948068, -79.095902),
                    new google.maps.LatLng(35.948061, -79.095814),
                    new google.maps.LatLng(35.948061, -79.095798),
                    new google.maps.LatLng(35.948060, -79.095764),
                    new google.maps.LatLng(35.948053, -79.095697),
                    new google.maps.LatLng(35.948049, -79.095613),
                    new google.maps.LatLng(35.948039, -79.095550),
                    new google.maps.LatLng(35.948040, -79.095422),
                    new google.maps.LatLng(35.948034, -79.095311),
                    new google.maps.LatLng(35.948032, -79.095212),
                    new google.maps.LatLng(35.948027, -79.095088),
                    new google.maps.LatLng(35.948023, -79.094966),
                    new google.maps.LatLng(35.948022, -79.094943),
                    new google.maps.LatLng(35.948025, -79.094817),
                    new google.maps.LatLng(35.948023, -79.094793),
                    new google.maps.LatLng(35.948022, -79.094652),
                    new google.maps.LatLng(35.948013, -79.094537),
                    new google.maps.LatLng(35.948026, -79.094383),
                    new google.maps.LatLng(35.948046, -79.094250),
                    new google.maps.LatLng(35.948078, -79.094161),
                    new google.maps.LatLng(35.948127, -79.094020),
                    new google.maps.LatLng(35.948165, -79.093898),
                    new google.maps.LatLng(35.948215, -79.093757),
                    new google.maps.LatLng(35.948285, -79.093621),
                    new google.maps.LatLng(35.948378, -79.093505),
                    new google.maps.LatLng(35.948472, -79.093396),
                    new google.maps.LatLng(35.948583, -79.093286),
                    new google.maps.LatLng(35.948652, -79.093216),
                    new google.maps.LatLng(35.948732, -79.093164),
                    new google.maps.LatLng(35.948851, -79.093063),
                    new google.maps.LatLng(35.948951, -79.092974),
                    new google.maps.LatLng(35.949042, -79.092876),
                    new google.maps.LatLng(35.949150, -79.092784),
                    new google.maps.LatLng(35.949245, -79.092701),
                    new google.maps.LatLng(35.949359, -79.092608),
                    new google.maps.LatLng(35.949474, -79.092499),
                    new google.maps.LatLng(35.949559, -79.092429),
                    new google.maps.LatLng(35.949639, -79.092364),
                    new google.maps.LatLng(35.949756, -79.092264),
                    new google.maps.LatLng(35.949841, -79.092177),
                    new google.maps.LatLng(35.949932, -79.092098),
                    new google.maps.LatLng(35.950012, -79.092024),
                    new google.maps.LatLng(35.950156, -79.091933),
                    new google.maps.LatLng(35.950281, -79.091896),
                    new google.maps.LatLng(35.950487, -79.091908),
                    new google.maps.LatLng(35.950607, -79.091975),
                    new google.maps.LatLng(35.950733, -79.092109),
                    new google.maps.LatLng(35.950807, -79.092256),
                    new google.maps.LatLng(35.950914, -79.092479),
                    new google.maps.LatLng(35.950978, -79.092637),
                    new google.maps.LatLng(35.951065, -79.092837),
                    new google.maps.LatLng(35.951125, -79.092998),
                    new google.maps.LatLng(35.951217, -79.093141),
                    new google.maps.LatLng(35.951341, -79.093241),
                    new google.maps.LatLng(35.951486, -79.093192),
                    new google.maps.LatLng(35.951671, -79.093086),
                    new google.maps.LatLng(35.951824, -79.093000),
                    new google.maps.LatLng(35.951954, -79.093014),
                ]
            });
    
        }
    </script>
    </head>
    <body style="margin:0px; padding:0px;" onload="initialize()">
        <div id="map_canvas" style="width: 100%; height: 100%;" />
    </body>
    </html>




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


Exploring sessions
==================

The package ``runpandas`` provides utilities to import a group of
activities data, and after careful processing, organises them into a
MultiIndex Dataframe.

The ``pandas.MultiIndex`` allows you to have multiple columns acting as
a row identifier and multiple rows acting as a header identifier. In our
scenario we will have as first indentifier (index) the timestamp of the
workout when it started, and as second indentifier the timedelta of the
consecutive observations of the workout.

.. figure:: MultiIndexDataframe.png
   :alt: Illustration of the MultiIndex Dataframe

   The MultiIndex Runpandas Activity Dataframe

The MultiIndex dataframe result from the function
``runpandas.read_dir_aggregate``, which takes as input the directory of
tracking data files, and constructs using the read*() functions to build
``runpandas.Activity`` objects. Them, the result daframes are first
sorted by the time stamps and are all combined into a single
``runpandas.Activity`` indexed by the two-level ``pandas.MultiIndex``.

Let’s illustrate these examples by loading a bunch of 68 running
activities of a female runner over the years of 2020 until 2021.

.. code:: ipython3

    import warnings
    warnings.filterwarnings('ignore')

.. code:: ipython3

    import runpandas
    session = runpandas.read_dir_aggregate(dirname='session/')

.. code:: ipython3

    session




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
          <th></th>
          <th>alt</th>
          <th>hr</th>
          <th>lon</th>
          <th>lat</th>
        </tr>
        <tr>
          <th>start</th>
          <th>time</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">2020-08-30 09:08:51.012</th>
          <th>00:00:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893609</td>
          <td>-8.045055</td>
        </tr>
        <tr>
          <th>00:00:01.091000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893624</td>
          <td>-8.045054</td>
        </tr>
        <tr>
          <th>00:00:02.091000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893641</td>
          <td>-8.045061</td>
        </tr>
        <tr>
          <th>00:00:03.098000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893655</td>
          <td>-8.045063</td>
        </tr>
        <tr>
          <th>00:00:04.098000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893655</td>
          <td>-8.045065</td>
        </tr>
        <tr>
          <th>...</th>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th rowspan="5" valign="top">2021-07-04 11:23:19.418</th>
          <th>00:52:39.582000</th>
          <td>0.050001</td>
          <td>189.0</td>
          <td>-34.894534</td>
          <td>-8.046602</td>
        </tr>
        <tr>
          <th>00:52:43.582000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.894465</td>
          <td>-8.046533</td>
        </tr>
        <tr>
          <th>00:52:44.582000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.894443</td>
          <td>-8.046515</td>
        </tr>
        <tr>
          <th>00:52:45.582000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.894429</td>
          <td>-8.046494</td>
        </tr>
        <tr>
          <th>00:52:49.582000</th>
          <td>NaN</td>
          <td>190.0</td>
          <td>-34.894395</td>
          <td>-8.046398</td>
        </tr>
      </tbody>
    </table>
    <p>48794 rows × 4 columns</p>
    </div>



Now let’s see how many activities there are available for analysis. For
this question, we also have an acessor
``runpandas.types.acessors.session._SessionAcessor`` that holds several
methods for computing the basic running metrics across all the
activities from this kind of frame and some summary statistics.

.. code:: ipython3

    #count the number of activities in the session
    print ('Total Activities:', session.session.count())


.. parsed-literal::

    Total Activities: 68


We might compute the main running metrics (speed, pace, moving, etc)
using the session acessors methods as like the ones available in the
``runpandas.types.metrics.MetricsAcessor`` . By the way, those methods
are called inside each metric method, but applying in each of activities
separatedely.

.. code:: ipython3

    #In this example we compute the distance and the distance per position across all workouts
    session = session.session.distance()
    session




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
          <th></th>
          <th>alt</th>
          <th>hr</th>
          <th>lon</th>
          <th>lat</th>
          <th>distpos</th>
          <th>dist</th>
        </tr>
        <tr>
          <th>start</th>
          <th>time</th>
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
          <th rowspan="5" valign="top">2020-08-30 09:08:51.012</th>
          <th>00:00:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893609</td>
          <td>-8.045055</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>00:00:01.091000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893624</td>
          <td>-8.045054</td>
          <td>1.690587</td>
          <td>1.690587</td>
        </tr>
        <tr>
          <th>00:00:02.091000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893641</td>
          <td>-8.045061</td>
          <td>2.095596</td>
          <td>3.786183</td>
        </tr>
        <tr>
          <th>00:00:03.098000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893655</td>
          <td>-8.045063</td>
          <td>1.594298</td>
          <td>5.380481</td>
        </tr>
        <tr>
          <th>00:00:04.098000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.893655</td>
          <td>-8.045065</td>
          <td>0.163334</td>
          <td>5.543815</td>
        </tr>
        <tr>
          <th>...</th>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th rowspan="5" valign="top">2021-07-04 11:23:19.418</th>
          <th>00:52:39.582000</th>
          <td>0.050001</td>
          <td>189.0</td>
          <td>-34.894534</td>
          <td>-8.046602</td>
          <td>12.015437</td>
          <td>8220.018885</td>
        </tr>
        <tr>
          <th>00:52:43.582000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.894465</td>
          <td>-8.046533</td>
          <td>10.749779</td>
          <td>8230.768664</td>
        </tr>
        <tr>
          <th>00:52:44.582000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.894443</td>
          <td>-8.046515</td>
          <td>3.163638</td>
          <td>8233.932302</td>
        </tr>
        <tr>
          <th>00:52:45.582000</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>-34.894429</td>
          <td>-8.046494</td>
          <td>2.851535</td>
          <td>8236.783837</td>
        </tr>
        <tr>
          <th>00:52:49.582000</th>
          <td>NaN</td>
          <td>190.0</td>
          <td>-34.894395</td>
          <td>-8.046398</td>
          <td>11.300740</td>
          <td>8248.084577</td>
        </tr>
      </tbody>
    </table>
    <p>48794 rows × 6 columns</p>
    </div>



.. code:: ipython3

    #comput the speed for each activity
    session = session.session.speed(from_distances=True)
    #compute the pace for each activity
    session = session.session.pace()
    #compute the inactivity periods for each activity
    session = session.session.only_moving()

After all the computation done, let’s going to the next step: the
exploration and get some descriptive statistics.

After the loading and metrics computation for all the activities, now
let’s look further the data and get the basic summaries about the
session: time spent, total distance, mean speed and other insightful
statistics in each running activity. For this task, we may accomplish it
by calling the method
``runpandas.types.session._SessionAcessor.summarize`` . It will return a
basic Dataframe including all the aggregated statistics per activity
from the season frame.

.. code:: ipython3

    summary = session.session.summarize()
    summary




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
          <th>moving_time</th>
          <th>mean_speed</th>
          <th>max_speed</th>
          <th>mean_pace</th>
          <th>max_pace</th>
          <th>mean_moving_speed</th>
          <th>mean_moving_pace</th>
          <th>mean_cadence</th>
          <th>max_cadence</th>
          <th>mean_moving_cadence</th>
          <th>mean_heart_rate</th>
          <th>max_heart_rate</th>
          <th>mean_moving_heart_rate</th>
          <th>mean_temperature</th>
          <th>min_temperature</th>
          <th>max_temperature</th>
          <th>total_distance</th>
          <th>ellapsed_time</th>
        </tr>
        <tr>
          <th>start</th>
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
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2020-07-03 09:50:53.162</th>
          <td>00:25:29.838000</td>
          <td>2.642051</td>
          <td>4.879655</td>
          <td>00:06:18</td>
          <td>00:03:24</td>
          <td>2.665008</td>
          <td>00:06:15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>178.819923</td>
          <td>188.0</td>
          <td>178.872587</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>4089.467333</td>
          <td>00:25:47.838000</td>
        </tr>
        <tr>
          <th>2020-07-05 09:33:20.999</th>
          <td>00:05:04.999000</td>
          <td>2.227637</td>
          <td>6.998021</td>
          <td>00:07:28</td>
          <td>00:02:22</td>
          <td>3.072098</td>
          <td>00:05:25</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>168.345455</td>
          <td>176.0</td>
          <td>168.900000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>980.162640</td>
          <td>00:07:20.001000</td>
        </tr>
        <tr>
          <th>2020-07-05 09:41:59.999</th>
          <td>00:18:19</td>
          <td>1.918949</td>
          <td>6.563570</td>
          <td>00:08:41</td>
          <td>00:02:32</td>
          <td>2.729788</td>
          <td>00:06:06</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>173.894180</td>
          <td>185.0</td>
          <td>174.577143</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3139.401118</td>
          <td>00:27:16</td>
        </tr>
        <tr>
          <th>2020-07-13 09:13:58.718</th>
          <td>00:40:21.281000</td>
          <td>2.509703</td>
          <td>8.520387</td>
          <td>00:06:38</td>
          <td>00:01:57</td>
          <td>2.573151</td>
          <td>00:06:28</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>170.808176</td>
          <td>185.0</td>
          <td>170.795527</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>6282.491059</td>
          <td>00:41:43.281000</td>
        </tr>
        <tr>
          <th>2020-07-17 09:33:02.308</th>
          <td>00:32:07.691000</td>
          <td>2.643278</td>
          <td>8.365431</td>
          <td>00:06:18</td>
          <td>00:01:59</td>
          <td>2.643278</td>
          <td>00:06:18</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>176.436242</td>
          <td>186.0</td>
          <td>176.436242</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>5095.423045</td>
          <td>00:32:07.691000</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2021-06-13 09:22:30.985</th>
          <td>01:32:33.018000</td>
          <td>2.612872</td>
          <td>23.583956</td>
          <td>00:06:22</td>
          <td>00:00:42</td>
          <td>2.810855</td>
          <td>00:05:55</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>169.340812</td>
          <td>183.0</td>
          <td>169.655879</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>15706.017295</td>
          <td>01:40:11.016000</td>
        </tr>
        <tr>
          <th>2021-06-20 09:16:55.163</th>
          <td>00:59:44.512000</td>
          <td>2.492640</td>
          <td>6.065895</td>
          <td>00:06:41</td>
          <td>00:02:44</td>
          <td>2.749453</td>
          <td>00:06:03</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>170.539809</td>
          <td>190.0</td>
          <td>171.231392</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>9965.168311</td>
          <td>01:06:37.837000</td>
        </tr>
        <tr>
          <th>2021-06-23 09:37:44.000</th>
          <td>00:26:49.001000</td>
          <td>2.501796</td>
          <td>5.641343</td>
          <td>00:06:39</td>
          <td>00:02:57</td>
          <td>2.568947</td>
          <td>00:06:29</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>156.864865</td>
          <td>171.0</td>
          <td>156.957031</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>4165.492241</td>
          <td>00:27:45.001000</td>
        </tr>
        <tr>
          <th>2021-06-27 09:50:08.664</th>
          <td>00:31:42.336000</td>
          <td>2.646493</td>
          <td>32.734124</td>
          <td>00:06:17</td>
          <td>00:00:30</td>
          <td>2.661853</td>
          <td>00:06:15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>166.642857</td>
          <td>176.0</td>
          <td>166.721116</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>5074.217061</td>
          <td>00:31:57.336000</td>
        </tr>
        <tr>
          <th>2021-07-04 11:23:19.418</th>
          <td>00:47:47.583000</td>
          <td>2.602263</td>
          <td>4.212320</td>
          <td>00:06:24</td>
          <td>00:03:57</td>
          <td>2.856801</td>
          <td>00:05:50</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>177.821862</td>
          <td>192.0</td>
          <td>177.956967</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>8248.084577</td>
          <td>00:52:49.582000</td>
        </tr>
      </tbody>
    </table>
    <p>68 rows × 18 columns</p>
    </div>



.. code:: ipython3

    print('Session Interval:', (summary.index.to_series().max() - summary.index.to_series().min()).days, 'days')
    print('Total Workouts:', len(summary), 'runnings')
    print('Tota KM Distance:', summary['total_distance'].sum() / 1000)
    print('Average Pace (all runs):', summary.mean_pace.mean())
    print('Average Moving Pace (all runs):', summary.mean_moving_pace.mean())
    print('Average KM Distance (all runs):', round(summary.total_distance.mean()/ 1000,2))


.. parsed-literal::

    Session Interval: 366 days
    Total Workouts: 68 runnings
    Tota KM Distance: 491.77377537338896
    Average Pace (all runs): 0 days 00:07:18.411764
    Average Moving Pace (all runs): 0 days 00:06:02.147058
    Average KM Distance (all runs): 7.23


At this point, I have the summary data to start some powerful
visualization and analysis. At the charts below we illustrate her pace
and distance evolution over time.

.. code:: ipython3

    import matplotlib.pyplot as plt
    import datetime
    
    #let's convert the pace to float number in minutes
    summary['mean_moving_pace_float'] = summary['mean_moving_pace'] / datetime.timedelta(minutes=1)
    summary['pace_moving_all_mean'] = summary.mean_moving_pace.mean()
    summary['pace_moving_all_mean_float'] = summary['pace_moving_all_mean'] / datetime.timedelta(minutes=1)
    
    plt.subplots(figsize=(8, 5))
    
    plt.plot(summary.index, summary.mean_moving_pace_float, color='silver')
    plt.plot(summary.pace_moving_all_mean_float, color='purple', linestyle='dashed', label='average')
    plt.title("Pace Evolution")
    plt.xlabel("Runnings")
    plt.ylabel("Pace")
    plt.legend()




.. parsed-literal::

    <matplotlib.legend.Legend at 0x7f82d8d83cd0>




.. image:: overview_files/overview_56_1.svg


.. code:: ipython3

    
    plt.subplots(figsize=(8, 5))
    
    summary['distance_all_mean'] = round(summary.total_distance.mean()/1000,2)
    
    plt.plot(summary.index, summary.total_distance / 1000, color='silver')
    plt.plot(summary.distance_all_mean, color='purple', linestyle='dashed', label='average')
    plt.title("Distance Evolution")
    plt.xlabel("Runs")
    plt.ylabel("distance")
    plt.legend()
    
    
    plt.show()



.. image:: overview_files/overview_57_0.svg


