from collections import defaultdict, namedtuple
import csv
import matplotlib.pyplot as plt
import numpy as np

#TODO(chas): I should probably use pandas for this instead
Sample = namedtuple('Sample', ['time', 'value'])
TimeSeries = namedtuple('TimeSeries', ['times', 'values'])

samples = {0:defaultdict(list), 1:defaultdict(list), 2:defaultdict(list),
           3:defaultdict(list), 'accel':defaultdict(list)}

def plot(ax, timeseries, label, color=None):
    ax.plot(timeseries[label].times, timeseries[label].values, label=label, color=color)

with open('test-spin-weapons.csv', newline='') as csvfile:
    weapon_vescs = csv.reader(csvfile)
    for (time, vesc, param, value) in weapon_vescs:
        samples[int(vesc)][param.strip()].append(Sample(float(time)/1000.0, value))

with open('test-spin-accel.csv', newline='') as csvfile:
    accel = csv.reader(csvfile)
    for (time, x, y, z) in accel:
        t = float(time)/1000.0
        samples['accel']['x'].append(Sample(t, x))
        samples['accel']['y'].append(Sample(t, y))
        samples['accel']['z'].append(Sample(t, z))

timeseries = {0:{}, 1:{}, 'accel':{}}
for (index, data) in samples.items():
    for (param, datapoints) in data.items():
        times = np.array([float(point.time) for point in datapoints])
        values = np.array([float(point.value) for point in datapoints])
        timeseries[index][param] = TimeSeries(times, values)

timeseries['accel']['abs_accel'] = TimeSeries(timeseries['accel']['x'].times,
                                            3 * np.sqrt(timeseries[index]['x'].values**2 +
                                                    timeseries[index]['y'].values**2 +
                                                    timeseries[index]['z'].values**2
                                                    ))
for index in range(2):
    timeseries[index]['avg_i_abs'] = TimeSeries(timeseries[index]['avg_iq'].times,
                                                np.sqrt(timeseries[index]['avg_iq'].values**2 +
                                                        timeseries[index]['avg_id'].values**2))

for index in range(2):
    # RPM is in ERPM, 7 motor pole pairs and a 4.1:1 gear reduction gets you to weapon rpm
    timeseries[index]['rpm'] = TimeSeries(timeseries[index]['rpm'].times, np.abs(timeseries[index]['rpm'].values/(4.1*7)))
    # This is just so to see the fault codes on the time graph.
    # TODO(chas): add the name of the fault code
    timeseries[index]['mc_fault_code'] = TimeSeries(timeseries[index]['mc_fault_code'].times, timeseries[index]['mc_fault_code'].values*10.0)

# todo(cleichner): fix scaling
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.set_title('Test Spin')
ax.set_xlabel('Time since drive turned on (s)')
ax.set_ylabel('arbitrary units (current is true to scale)')
plot(ax, timeseries[0],'avg_i_abs')
#plot(ax, timeseries[0],'avg_id')
#plot(ax, timeseries[0],'avg_iq')
plot(ax, timeseries[0],'mc_fault_code')
#plot(ax, timeseries[0],'temp_fet')
#plot(ax, timeseries[0],'v_in')
plot(ax, timeseries[1],'avg_i_abs')
plot(ax, timeseries[1],'mc_fault_code')
#plot(ax, timeseries[1],'temp_fet')
#plot(ax, timeseries['accel'],'abs_accel')
plot(ax, timeseries['accel'],'z')
plot(ax, timeseries['accel'],'y')
plot(ax, timeseries['accel'],'x')
plt.legend()
rpm_ax = ax.twinx()  # instantiate a second axes that shares the same x-axis
rpm_ax.set_ylabel('weapon rpm')
plot(rpm_ax, timeseries[0],'rpm', color='black')
plt.legend()
plt.show()

'''
const char* mc_interface_fault_to_string(mc_fault_code fault) {
	switch (fault) {
	case FAULT_CODE_NONE: return "FAULT_CODE_NONE"; break;
	case FAULT_CODE_OVER_VOLTAGE: return "FAULT_CODE_OVER_VOLTAGE"; break;
	case FAULT_CODE_UNDER_VOLTAGE: return "FAULT_CODE_UNDER_VOLTAGE"; break;
	case FAULT_CODE_DRV: return "FAULT_CODE_DRV"; break;
	case FAULT_CODE_ABS_OVER_CURRENT: return "FAULT_CODE_ABS_OVER_CURRENT"; break;
	case FAULT_CODE_OVER_TEMP_FET: return "FAULT_CODE_OVER_TEMP_FET"; break;
	case FAULT_CODE_OVER_TEMP_MOTOR: return "FAULT_CODE_OVER_TEMP_MOTOR"; break;
	case FAULT_CODE_GATE_DRIVER_OVER_VOLTAGE: return "FAULT_CODE_GATE_DRIVER_OVER_VOLTAGE"; break;
	case FAULT_CODE_GATE_DRIVER_UNDER_VOLTAGE: return "FAULT_CODE_GATE_DRIVER_UNDER_VOLTAGE"; break;
	case FAULT_CODE_MCU_UNDER_VOLTAGE: return "FAULT_CODE_MCU_UNDER_VOLTAGE"; break;
	case FAULT_CODE_BOOTING_FROM_WATCHDOG_RESET: return "FAULT_CODE_BOOTING_FROM_WATCHDOG_RESET"; break;
	case FAULT_CODE_ENCODER_SPI: return "FAULT_CODE_ENCODER_SPI"; break;
	case FAULT_CODE_ENCODER_SINCOS_BELOW_MIN_AMPLITUDE: return "FAULT_CODE_ENCODER_SINCOS_BELOW_MIN_AMPLITUDE"; break;
	case FAULT_CODE_ENCODER_SINCOS_ABOVE_MAX_AMPLITUDE: return "FAULT_CODE_ENCODER_SINCOS_ABOVE_MAX_AMPLITUDE"; break;
    case FAULT_CODE_FLASH_CORRUPTION: return "FAULT_CODE_FLASH_CORRUPTION";
    case FAULT_CODE_HIGH_OFFSET_CURRENT_SENSOR_1: return "FAULT_CODE_HIGH_OFFSET_CURRENT_SENSOR_1";
    case FAULT_CODE_HIGH_OFFSET_CURRENT_SENSOR_2: return "FAULT_CODE_HIGH_OFFSET_CURRENT_SENSOR_2";
    case FAULT_CODE_HIGH_OFFSET_CURRENT_SENSOR_3: return "FAULT_CODE_HIGH_OFFSET_CURRENT_SENSOR_3";
    case FAULT_CODE_UNBALANCED_CURRENTS: return "FAULT_CODE_UNBALANCED_CURRENTS";
    case FAULT_CODE_BRK: return "FAULT_CODE_BRK";
	default: return "FAULT_UNKNOWN"; break;
	}
'''
