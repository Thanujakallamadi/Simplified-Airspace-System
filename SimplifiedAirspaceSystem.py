# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:50:24 2019

@author: kalla
"""
import pandas as pd
# function to convert the time into 24 hour format
def ConvertTimeTo24HourFormat(t):
    if 'AM' in t.upper() and '12' in t.split(':')[0]:
        ConvertedTime = 0
    elif 'AM' in t.split(':')[1].upper():
        ConvertedTime = int(t.split(':')[0])
    elif 'PM' in t.upper() and '12' in t.split(':')[0]:
        ConvertedTime = 12
    elif 'AM' not in t.upper() and 'PM' not in t.upper():
        ConvertedTime = int(t.split(':')[0])
    else:
        ConvertedTime = int(t.split(':')[0])+12
        
    
    minutes = int(t.split(':')[1].split(' ')[0])
    
    Exact_time = ConvertedTime * 60 + minutes
    
    if minutes >= 30 and ConvertedTime != 23:
        ConvertedTime = ConvertedTime + 1
    return Exact_time,ConvertedTime

if __name__=="__main__":
    minimun_capacity = 9999999
    maximum_capacity = 0
    
    #initializing the dictionary with 24 states(as 24 hours needs to be considered)
    
    Time_Space_Dictionary = {0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{},14:{},15:{},16:{},17:{},18:{},19:{},20:{},21:{},22:{},23:{}}
    
    #initializing lists
    
    for k in range(0,24):
        Time_Space_Dictionary[k]["Flight_Numbers"] = []
        Time_Space_Dictionary[k]["StartFlightDetails"] = []
        Time_Space_Dictionary[k]["ReachedFlightDetails"] = []
        Time_Space_Dictionary[k]["Start_Locations"] = []
        Time_Space_Dictionary[k]["End_Locations"] = []
        
    #read the data from csv file
    data=pd.read_csv(r"DetailsOfFlights.csv")
    
   # data=pd.read_csv(r"GiveYourilePathHere.csv")
    
    #Capacity of the flights is stored in the dictionary CapacityOfFlights
    
    CapacityOfFlights = {"A220":105,"A319":128,"A320":150,"A321":185,"A321neo":196,"A330-200":230,"A330-300":290,"A330-900neo":280,"A350-900":300,"717-200":110,"737-700":126,"737-800":165,"737-900":180,"737-900ER":180,"737-Max 9": 180,"757-200":180,"757-300":230,"767-300":200,"767-300ER":225,"767-400ER": 240,"777-200":270,"777-200ER":270,"777-200LR": 280,"777-300": 300,"787-8": 235,"787-9": 280,"Embraer 170":72,"Embraer 175 (E 75)":78,"Embraer 190 ":100,"McDonnell Douglas MD-88": 150,"McDonnell Douglas MD-90-30": 150,"CRJ 700":75,"MD-88":150,"MD-90":150,"CRJ 900":75,"Canadair Regional Jet 900":75,"Canadair Regional Jet 700":75,"Embraer 175":78,"Embraer E175":78,"Embraer 175 (Enhanced Winglets)":75,"757-232":295,"757":295,"CRJ-200":50,"Boeing 717":134,"Bombardier CS100":145}
    
    capacityOfFlight = 0
    
    for i in range(0,data.shape[0]):
        departure_exact_time,departure_time = ConvertTimeTo24HourFormat(data.loc[i][2])
        
        #print("test",data.loc[i][4])
        
        #if capacity is given directly in csv it copies the value else it checks in the dictionary and stores the value
        
        try:
            if int(data.loc[i][4]):
                capacityOfFlight = data.loc[i][4]
        except ValueError:
                for j,value in enumerate(CapacityOfFlights.keys()):
                    if value in data.loc[i][4]:
                        try:
                            capacityOfFlight = int(CapacityOfFlights[value])
                        except TypeError:
                            capacityOfFlight = 0
                            
        arrival_exact_time,arrival_time = ConvertTimeTo24HourFormat(data.loc[i][3])
        #print(arrival_time)
        #print(departure_time)
        Time_Space_Dictionary[arrival_time]["Flight_Numbers"].append(data.loc[i][5])
        Time_Space_Dictionary[departure_time]["Flight_Numbers"].append(data.loc[i][5])
        Time_Space_Dictionary[departure_time]["StartFlightDetails"].append([data.loc[i][0],data.loc[i][1],capacityOfFlight,data.loc[i][5],departure_exact_time])
        Time_Space_Dictionary[arrival_time]["ReachedFlightDetails"].append([data.loc[i][0],data.loc[i][1],capacityOfFlight,data.loc[i][5],arrival_exact_time])
        Time_Space_Dictionary[departure_time]["Start_Locations"].append(data.loc[i][0])
        Time_Space_Dictionary[arrival_time]["End_Locations"].append(data.loc[i][1])
        
TotalCapacity = 0
while(1):
    visited = []
    path = []
    sourceCity = "LAX"
    destinationCity = ""
    flag0 = 0
    flag1 = 1
    minimum_capacity = 9999999
    flightNumber = ""
    for key,values in Time_Space_Dictionary.items():
        #if the source city is LAX
        if(sourceCity in values["Start_Locations"]) and (flag0==0) and (sourceCity not in visited):
            index = 0
            for j in values["StartFlightDetails"]:
                if sourceCity in j[0] and j[1] not in visited:
                    sourceCity = j[0]
                    destinationCity = j[1]
                    capacityOfFlight = j[2]
                    flightNumber = j[3]
                    flag0 = 1
                    flag1 = 0
                    visited.append(key)
                    visited.append(index)
                    visited.append(sourceCity)
                    visited.append(flightNumber)
                    path.append(sourceCity)
                    if(capacityOfFlight)<int(minimum_capacity):
                        minimum_capacity = capacityOfFlight
                    break
                index = index + 1
                #if the source city is not LAX and destination city is not JFK
        if flightNumber in values["Flight_Numbers"] and destinationCity in values["End_Locations"] and flag1==0 and destinationCity!="JFK":
            index = 0
            for j in values["ReachedFlightDetails"]:
                if j[1]==destinationCity and j[3]==flightNumber and j[1] not in visited:
                    sourceCity = j[1]
                    flag0 = 0
                    flag1 = 1
                    visited.append(key)
                    visited.append(index)
                    time_reached = j[4]
                    if(sourceCity in values["Start_Locations"]) and (flag0==0) and (sourceCity not in visited):
                        index = 0
                        for j in values["StartFlightDetails"]:
                            if sourceCity in j[0] and time_reached<j[4] and j[1] not in visited:
                                sourceCity = j[0]
                                destinationCity = j[1]
                                capacityOfFlight = j[2]
                                flightNumber = j[3]
                                flag0 = 1
                                flag1 = 0
                                visited.append(key)
                                visited.append(index)
                                visited.append(sourceCity)
                                visited.append(flightNumber)
                                path.append(sourceCity)
                                if capacityOfFlight < minimum_capacity:
                                    minimum_capacity = capacityOfFlight
                                break
                            index = index + 1
                    break
                index = index + 1
        # if the destination city is JFK
        if destinationCity=="JFK":
            TotalCapacity= TotalCapacity+ minimum_capacity
            path.append(destinationCity)
            #print("Found: Flights to destination\t",visited,"\n")
            print("Capacity:",minimum_capacity,"\n")
            
            print("Final path:",path,"\n")
            j = 0
            x = 0
            visitedLength = len(visited)
            while j < visitedLength:
                if x%2 == 0:
                    Time_Space_Dictionary[visited[j]]["StartFlightDetails"][visited[j+1]][2]-=minimum_capacity
                    if Time_Space_Dictionary[visited[j]]["StartFlightDetails"][visited[j+1]][2]==0:
                        Time_Space_Dictionary[visited[j]]["Start_Locations"].remove(visited[j+2])
                        Time_Space_Dictionary[visited[j]]["Flight_Numbers"].remove(visited[j+3])
                        Time_Space_Dictionary[visited[j]]["StartFlightDetails"]=Time_Space_Dictionary[visited[j]]["StartFlightDetails"][0:visited[j+1]]+Time_Space_Dictionary[visited[j]]["StartFlightDetails"][visited[j+1]+1:]
                    j = j + 4
                else:
                    Time_Space_Dictionary[visited[j]]["ReachedFlightDetails"][visited[j+1]][2]-=minimum_capacity
                    if Time_Space_Dictionary[visited[j]]["ReachedFlightDetails"][visited[j+1]][2]==0:
                        Time_Space_Dictionary[visited[j]]["End_Locations"].remove(visited[j+4])
                        Time_Space_Dictionary[visited[j]]["Flight_Numbers"].remove(visited[j-1])
                        Time_Space_Dictionary[visited[j]]["ReachedFlightDetails"]=Time_Space_Dictionary[visited[j]]["ReachedFlightDetails"][0:visited[j+1]]+Time_Space_Dictionary[visited[j]]["ReachedFlightDetails"][visited[j+1]+1:]
                    j = j + 2
                x = x + 1
            break
    #if the destination city is not JFK
    if destinationCity != "JFK":
            #print("Not Found: Flights to destination\t:",visited,"\n")
            visitedLength = len(visited)
            if visitedLength == 0:
                print("Total capacity:",TotalCapacity)
                break
            
            Time_Space_Dictionary[visited[visitedLength-2]]["End_Locations"].remove(Time_Space_Dictionary[visited[visitedLength-2]]["ReachedFlightDetails"][visited[visitedLength-1]][1])
            Time_Space_Dictionary[visited[visitedLength-2]]["Flight_Numbers"].remove(visited[visitedLength-3])
            Time_Space_Dictionary[visited[visitedLength-2]]["ReachedFlightDetails"]=Time_Space_Dictionary[visited[visitedLength-2]]["ReachedFlightDetails"][0:visited[visitedLength-1]]+ Time_Space_Dictionary[visited[visitedLength-2]]["ReachedFlightDetails"][visited[visitedLength-1]+1:]
            Time_Space_Dictionary[visited[visitedLength-6]]["Start_Locations"].remove(visited[visitedLength-4])
            Time_Space_Dictionary[visited[visitedLength-6]]["Flight_Numbers"].remove(visited[visitedLength-3])
            Time_Space_Dictionary[visited[visitedLength-6]]["StartFlightDetails"]=Time_Space_Dictionary[visited[visitedLength-6]]["StartFlightDetails"][0:visited[visitedLength-5]]+Time_Space_Dictionary[visited[visitedLength-6]]["StartFlightDetails"][visited[visitedLength-5]+1:]
            