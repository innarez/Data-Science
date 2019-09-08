import pandas as pd
import json
import sys
import csv
import requests
import os 
import math

#function for getting the distances in commands 4 and 5
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p)*math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p)) / 2
    return 12742 * math.asin(math.sqrt(a))

#determine how many arguments entered
args_size = len(sys.argv)

#assign baseURL and the command to variables
baseURL = sys.argv[1]
command = sys.argv[2]

#assign parameter variables if possible
if args_size == 4:
    param1 = sys.argv[3]
elif args_size == 5:
    param1 = sys.argv[3]
    param2 = sys.argv[4]
elif args_size > 5:
    print("Too many arugments entered.")

#------------------------------------------------------------------------------
#Command #1: Total Bikes Available (total_bikes)
if command == "total_bikes":    
    baseURL += "station_status.json"
    file = requests.get(baseURL)
    j_data = json.loads(file.content)
    
    #converting json file to csv
    with open('station_data.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["station_id","num_bikes_available","num_docks_available",
                         "is_installed", "is_renting","is_returning", "last_reported"])
        for line in j_data["data"]["stations"]:
            writer.writerow([line["station_id"], line["num_bikes_available"],
                               line["num_docks_available"], line["is_installed"],
                                line["is_renting"], line["is_returning"], 
                                line["last_reported"]])

    #calculate the sum of available bikes
    result = 0
    reader = open('station_data.csv', 'rt')
    csv_reader = csv.DictReader(reader)
    for row in csv_reader:
        result += int(row["num_bikes_available"])
    reader.close()
    
    #print the output
    print("")
    print("Command=", command, sep="")
    print("Parameters=")
    print("Output=",result, sep="")
    print("")
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#Command #2: Total Docks Available
if command == "total_docks":       
    baseURL += "station_status.json"
    file = requests.get(baseURL)
    j_data = json.loads(file.content)
    
    #converting json file to csv
    with open('station_data.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["station_id","num_bikes_available","num_docks_available",
                         "is_installed", "is_renting","is_returning", "last_reported"])
        for line in j_data["data"]["stations"]:
            writer.writerow([line["station_id"], line["num_bikes_available"],
                               line["num_docks_available"], line["is_installed"],
                                line["is_renting"], line["is_returning"], 
                                line["last_reported"]])

    #calculate the sum of docks
    result = 0
    reader = open('station_data.csv', 'rt')
    csv_reader = csv.DictReader(reader)
    for row in csv_reader:
        result += int(row["num_docks_available"])
    reader.close()
    
    #print the result
    print("")
    print("Command=", command, sep="")
    print("Parameters=")
    print("Output=",result, sep="")  
    print("")
    
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#Command #3: Percentage of Docks available at station
if command == "percent_avail":
    baseURL += "station_status.json"
    file = requests.get(baseURL)
    j_data = json.loads(file.content)
    
    #converting json file to csv
    with open('station_data.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["station_id","num_bikes_available","num_docks_available",
                         "is_installed", "is_renting","is_returning", "last_reported"])
        for line in j_data["data"]["stations"]:
            writer.writerow([line["station_id"], line["num_bikes_available"],
                               line["num_docks_available"], line["is_installed"],
                                line["is_renting"], line["is_returning"], 
                                line["last_reported"]])

    
    #determine the percentage of docks available ( = docks/ (docks+bikes))
    result = 0
    docks = 0
    bikes = 0
    reader = open('station_data.csv', 'rt')
    csv_reader = csv.reader(reader)
    for row in csv_reader:
        if param1 in row:
            for field in row:
                bikes = int(row[1])
                docks = int(row[2])               
            result = (docks/(docks + bikes))*100
            break
    reader.close()
    
    
    #print the result
    print("")
    print("Command=", command, sep="")
    print("Parameters=", param1, sep="")
    print("Output=",int(round(result)), "%", sep="") 
    print("")
#------------------------------------------------------------------------------    


   

#------------------------------------------------------------------------------    
#Command #4: Name of three closest HealthyRidePGH stations
if command == "closest_stations":
    baseURL += "station_information.json"
    file = requests.get(baseURL)
    j_data = json.loads(file.content)
    
    #converting json file to csv
    with open('station_info.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["station_id","name","short_name", "lat", "lon", 
                         "region_id","capacity"])
        for line in j_data["data"]["stations"]:
            writer.writerow([line["station_id"], line["name"],line["short_name"],
                             line["lat"],line["lon"], line["region_id"], 
                             line["capacity"]])
    
    #initialize variables
    id1 = 0
    id2 = 0
    id3 = 0
    name1 = ""
    name2 = ""
    name3 = ""
    first = math.inf
    second = math.inf
    third = math.inf
    
    #determine the top three closest bike stations 
    reader = open('station_info.csv', 'rt')
    csv_reader = csv.DictReader(reader)
    for row in csv_reader:
        d = distance(float(param1),float(param2),float(row["lat"]),float(row["lon"]))
        if d < third:
            if d < second:
                if d < first:
                   t1 = first
                   t2 = second
                   first = d
                   second = t1
                   third = t2
                   id3 = id2
                   name3 = name2
                   id2 = id1
                   name2 = name1
                   id1 = row["station_id"]
                   name1 = row["name"]  
                else:  
                   t1 = second
                   second = d
                   third = t1
                   id3 = id2
                   name3 = name2
                   id2 = row["station_id"]
                   name2 = row["name"]
            else:            
                third = d
                id3 = row["station_id"]
                name3 = row["name"]
        else:
            continue
    reader.close()  
    
    
    
    #print the result
    print("")
    print("Command=", command, sep="")
    print("Parameters=", param1," ",param2, sep="")
    print("Output=") 
    print(id1,","," ",name1, sep="")
    print(id2,",", " ", name2, sep="")
    print(id3,",", " ", name3, sep="")
    print("")

#------------------------------------------------------------------------------






#------------------------------------------------------------------------------
#Command 5: Name of closest HealthyRidePGH station w/ available bikes
if command == "closest_bike":
    baseURL1 = baseURL + "station_information.json"
    baseURL2 = baseURL + "station_status.json"
    file1 = requests.get(baseURL1)
    file2 = requests.get(baseURL2)
    j_data1 = json.loads(file1.content.decode())
    j_data2 = json.loads(file2.content.decode())
    
    #converting json file to csv
    with open('station_info.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["station_id","name","short_name", "lat", "lon", 
                         "region_id","capacity"])
        for line in j_data1["data"]["stations"]:
            writer.writerow([line["station_id"], line["name"],line["short_name"],
                             line["lat"],line["lon"], line["region_id"], 
                             line["capacity"]])
    #convert other json to csv
    with open('station_data.csv', 'w') as out:
        writer = csv.writer(out)  
        writer.writerow(["station_id","num_bikes_available","num_docks_available",
                         "is_installed", "is_renting","is_returning", "last_reported"])       
        for line in j_data2["data"]["stations"]:
            writer.writerow([line["station_id"], line["num_bikes_available"],
                             line["num_docks_available"], line["is_installed"],
                             line["is_renting"], line["is_returning"], 
                             line["last_reported"]])
    
    #initialize variables
    id1 = 0
    id2 = 0
    name1 = ""
    first = math.inf
    bikes = 0
    
    reader1 = open('station_info.csv', 'rt')
    csv_reader1 = csv.DictReader(reader1)
    
    reader2 = open('station_data.csv', 'rt')
    csv_reader2 = csv.DictReader(reader2)
    
    #function to determine if bikes are available at that station
    def get_bikes(id2):
        for row in csv_reader2:
            if id2 == row["station_id"]:
                num = row["num_bikes_available"]
                return int(num)
    
    #determine the closest station and if it has available bikes
    for row in csv_reader1:
        d = distance(float(param1),float(param2),float(row["lat"]),float(row["lon"]))
        if d < first:
            id2 =row["station_id"]
            bike = get_bikes(id2)
            if bike > 0:
                id1 = id2
                name1 = row["name"]
                first = d
            else:
                continue
      
    #print the result
    print("")
    print("Command=", command, sep="")
    print("Parameters=", param1," ", param2, sep="")
    print("Output=", id1,","," ",name1, sep="") 
    print("")
    
  
#------------------------------------------------------------------------------    

