import numpy as np

# Speed from Google Maps (km/h)
speed_measured = np.array([
    0, 33, 29, 28, 8, 42, 30, 46, 0, 0, 0, 0, 0, 0,
    47, 42, 37, 51, 60, 57, 42, 0
])

# Distance covered each minute (km)
distance_each_min = speed_measured * (1 / 60)

# Speed calculated back from distance
speed_calculated = distance_each_min * 60

# Error calculations
absolute_error = np.abs(speed_measured - speed_calculated)
mean_error = np.mean(absolute_error)
rmse = np.sqrt(np.mean(absolute_error ** 2))

print("Absolute Error (km/h):", absolute_error)
print("Mean Error (km/h):", round(mean_error, 2))
print("RMSE (km/h):", round(rmse, 2))