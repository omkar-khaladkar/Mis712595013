import matplotlib.pyplot as plt
import numpy as np

# Time (minutes)
time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20.5]

# Speed (km/h)
speed = [0, 33, 29, 28, 8, 42, 30, 46, 0, 0, 0, 0, 0, 0, 47, 42, 37, 51, 60, 57, 42, 0]

# Acceleration (km/h per minute)
acceleration = np.diff(speed)

# Jerk (km/h per minute^2)
jerk = np.diff(acceleration)

time_jerk = time[2:]  # corresponding time values

plt.figure()
plt.plot(time_jerk, jerk, marker='o')
plt.xlabel("Time (minutes)")
plt.ylabel("Jerk (km/h per minute²)")
plt.title("Jerk vs Time")
plt.grid(True)
plt.show()