# Speed data (km/h)
speed = [0, 33, 29, 28, 8, 42, 30, 46, 0, 0, 0, 0, 0, 0, 47, 42, 37, 51, 60, 57, 42, 0]

# Time interval = 1 minute = 1/60 hour
distance_each_min = []

for s in speed:
    distance_each_min.append(s * (1/60))

# Total calculated distance
calculated_distance = sum(distance_each_min)

# Actual distance from Google Maps (ENTER YOUR VALUE HERE)
actual_distance = 10.0   # km

# Percentage error
percentage_error = abs(actual_distance - calculated_distance) / actual_distance * 100

print("Calculated distance (km):", round(calculated_distance, 2))
print("Actual distance (km):", actual_distance)
print("Percentage error (%):", round(percentage_error, 2))