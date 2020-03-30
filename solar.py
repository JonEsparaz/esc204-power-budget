import csv
import matplotlib.pyplot as plt

solar_panel_size = 0.19 #m^2
battery_capacity = 100 #Wh
cycle_usage = 5.46 #Wh
lower_limit = battery_capacity*0.2 #Wh
step_size = 15 #mins
step_size_hrs = step_size/60 #hrs
efficiency = 0.15

charge = 0.5*battery_capacity #init to 50% capacity
charges = [charge]
times = [0] #init at time zero
sun_data = []

#please ensure data is in CSV format
with open('Solar Power Data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader) #skip header
    for row in csv_reader:
        sun_data.append(row)

for data in sun_data:
    gain = solar_panel_size*int(data[2])*step_size_hrs*efficiency 
    charge += gain #increase charge based on solar irradiance, solar panel size and efficiency
    if (charge>battery_capacity): #check if maximum capacity has been reached
        charge = battery_capacity
    if data[3] == "1": #check if a plug-in cycle is to occur
        charge -= cycle_usage #decrease charge based on power consumption of a single plug-in cycle
    if charge < lower_limit: #check if less than 20% capacity
        print(r"Warning less than 20% capacity on day", data[0], "at", data[1]) #alert human
    charges.append(charge)

for i in range(0, len(sun_data)):
    times.append(times[i]+step_size)

lower_limit_plot = [] 
for i in times:
    lower_limit_plot.append(lower_limit)

tick_locs = []
time_labels = []
for i in range(0,len(sun_data)):
    if (i%24 == 0):
        time_labels.append(sun_data[i][1])
        tick_locs.append(times[i])

plt.plot(times,charges,'.-')
plt.plot(times,lower_limit_plot)
plt.xticks(tick_locs,time_labels,rotation=60)
plt.ylabel("Battery Capacity (Wh)")
plt.legend(["Battery Capacity","20% Capacity Limit"])
plt.show()
