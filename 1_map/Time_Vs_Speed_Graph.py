import matplotlib.pyplot as plt

# Time (in minutes)
time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20.5]

# Speed (in km/h)
speed = [0, 33, 29, 28, 8, 42, 30, 46, 0, 0, 0, 0, 0, 0, 47, 42, 37, 51, 60, 57, 42, 0]

plt.figure()
plt.plot(time, speed, marker='o')
plt.xlabel("Time (minutes)")
plt.ylabel("Speed (km/h)")
plt.title("Speed vs Time for Recorded Journey")
plt.grid(True)
plt.show()