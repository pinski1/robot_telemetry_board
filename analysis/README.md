This graphs telemetry logs.

Check the scale on the parameter you are interested in before reading it off
the graph, the first priority of these graphs was estabilishing time corolation
between the different logging systems e.g. accelerometer, rpm, and motor
controller faults.

Install the dependencies with `pip3 install -r requirements.txt`.

Pull the data file that you want to analyze off of the microSD card on the
microcontroller. Extract the data from the [realtime telemetry
system](https://github.com/mjg59/robot_telemetry) with the `./visualize.py`
script from that repository.

If the data file is called `test-spin.data`, then you can get all of the motor
controller data with
`./visualize.py vesc all test-spin.data test-spin-vescs.csv` and all of the
accelerometer data with `./visualize.py vesc accel test-spin.data test-spin-accel.csv`.

Visualize the result with `python3 analyis.py`.

The file names are currently hardcoded in the analysis.py, so if you want to do
a different analysis, you will need to edit that file.

The hardware also can log from four motor controllers, but we only had the two
weapon motors plugged in for the attached test, so you will have to add data
from `timeseries[2]` and `timeseries[3]` to the plotting at the bottom if you'd
like to graph all four.

This is very rough and early stage work and all of it is subject to change
(hopefully for the better).

