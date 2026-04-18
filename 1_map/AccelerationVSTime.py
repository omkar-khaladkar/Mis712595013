import matplotlib.pyplot as plt
import numpy as np

# Time (minutes)
time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20.5]

# Speed (km/h)
speed = [0, 33, 29, 28, 8, 42, 30, 46, 0, 0, 0, 0, 0, 0, 47, 42, 37, 51, 60, 57, 42, 0]

# Calculate acceleration (km/h per minute)
acceleration = np.diff(speed)  # delta speed
time_acc = time[1:]            # corresponding time values

plt.figure()
plt.plot(time_acc, acceleration, marker='o')
plt.xlabel("Time (minutes)")
plt.ylabel("Acceleration (km/h per minute)")
plt.title("Acceleration vs Time")
plt.grid(True)
plt.show()