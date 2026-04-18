import matplotlib.pyplot as plt

# Time (minutes)
time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20.5]

# Speed (km/h)
speed = [0, 33, 29, 28, 8, 42, 30, 46, 0, 0, 0, 0, 0, 0, 47, 42, 37, 51, 60, 57, 42, 0]

time_for_10km = []

for s in speed:
    if s == 0:
        time_for_10km.append(0)   # stop condition
    else:
        time_for_10km.append((10 / s) * 60)

plt.figure()
plt.plot(time, time_for_10km, marker='o')
plt.xlabel("Time (minutes)")
plt.ylabel("Time required to travel 10 km (minutes)")
plt.title("Instantaneous Time to Travel 10 km vs Time")
plt.grid(True)
plt.show()