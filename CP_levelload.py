"""Access data from Chargepoint API"""
#   Author: Sami Waheed
#   Date: September 2018
#
#   Overview:
#       This is an excerpt from a program used to run smart charging with ChargePoint charging stations. All ties related
#       to how the algorithm worked have been removed. Some examples of how to use the functions were left included.
#

from zeep import Client
from zeep.wsse.username import UsernameToken
import time as time

class CP_levelload:

    global client   # globally accessible variable for simplicity

    # Returns Station ID For All Stations Under the Account's Service Plan
    #   Used 'City' key since my account's only stations are in the same city
    #   index: the associated index from the list of ids (ids[] created in main)
    def get_stationID(index):
        response = (client.service.getStations(searchQuery={'City': 'enter yours'}))
        return response['stationData'][index]['stationID']


    # Returns Total Load (kW) at the Corresponding Station ID Passed In
    #   id: station ID of corresponding station
    def get_stationLoad(id):
        response = client.service.getLoad(searchQuery={'stationID': id})
        # print (response)
        return float(response['stationData'][0]['stationLoad'])


    # Returns Load (kW) for a Single Port (2 Ports Per Station)
    #   id: associated station
    #   portNum: 0 or 1
    def get_portLoad(id, portNum):
        response = client.service.getLoad(searchQuery={'stationID': id})
        # print (response)
        return float(response['stationData'][0]['Port'][portNum]['portLoad'])


    # Sets a Max Power for the Specified Station and Port
    #   portNum: 0 or 1
    #   timeInterval: 0 means to shed the load for no specified time
    #   allowedLoad: max power desired to set
    #   Note: expect up to a 5 minute delay in stations responding
    def setMaxPower(id, portNum, allowedLoad):
        client.service.shedLoad(shedQuery={'shedStation': {'stationID': id, 'Ports': {'Port': {
                                                            'portNumber': portNum,'allowedLoadPerPort': allowedLoad,
                                                            'percentShedPerPort': None}}}, 'timeInterval': 0})


    # Returns List of Station Group IDs
    #   Used 'City' key since my account's only stations are in the same city
    #   sgID: '112651', others are generic for Chargepoint
    def get_sgID():
        response = (client.service.getStations(searchQuery={'City': '***enter yours***'}))
        return response['stationData'][0]['sgID']


    # Clears All Max Powers Sent to Stations/Ports
    #   1 sgID was used since all stations were under the same station group ID (sgID) 
    #   Note: Expect up to a 10 minute delay in stations responding
    def clearSheds():
        client.service.clearShedState(shedQuery={'shedGroup': {'sgID': '***enter yours***'}})


    if __name__ == '__main__':
        while True:

            import datetime
            now = datetime.datetime.now()
            print ("Start:", now)

            # Initialize Zeep Client
            # Account info is for an "API User" Chargepoint account
            username = ''
            password = ''
            wsdl_url = 'https://webservices.chargepoint.com/cp_api_5.0.wsdl'
            client = Client(wsdl_url, wsse=UsernameToken(username, password))

            # Get Stations (all stations under my account were in the same city)
            stations = (client.service.getStations(searchQuery = {'City': '***enter yours***'}))
            # print (stations)

            # Get Station IDs
            ids = []
            for i in range(0,len(stations['stationData'])):
                tempID = get_stationID(i)
                ids.append(tempID)
            print ("Stations IDs: ", ids)

            # Get Current Load For Each Port (2 Ports/Station)
            currPower = []
            for i in ids:
                # Port 0
                portLoad0 = get_portLoad(i, 0)
                currPower.append(portLoad0)

                # Port 1
                portLoad1 = get_portLoad(i, 1)
                currPower.append(portLoad1)
            print ("Load before: ", currPower)
            EVLoad = sum(currPower)
            print ("EVLoad (kW): ", EVLoad)

            # Calculate Number of Cars Charging
            carsCharging = 0
            for i in range(0, len(currPower)):
                if currPower[i] != 0.0:
                    carsCharging += 1
            print ("Cars Charging: ", carsCharging)

            
            
                
            # Turn Off Chargers
            for i in ids:
                setMaxPower(i, 0, 0)
                setMaxPower(i, 1, 0)
                
            # Clear Any Load Sheds
            clearSheds()
               
            # Sets power to be 1.8 kW if a car was charging
            for i in range(0, len(currPower)):
                if currPower[i] < 1.8 and currPower[i] > 0:
                    currPower[i] = 1.8

             # If Port1 = 0 and Port2 != 0, sets both to nonzero value to avoid issue
             index = 0
             while index < len(currPower):
                 if currPower[index] == 0.0:
                     if currPower[index + 1] != 0.0:
                         currPower[index] = currPower[index + 1]
                 else:
                     if currPower[index + 1] == 0.0:
                         currPower[index + 1] = currPower[index]
                     index += 2

             # Set Max Powers Determined
             index = 0
             for i in ids:
                 # Port 1
                 setMaxPower(i, 0, currPower[index])
                 index += 1

                 # Port 2
                 setMaxPower(i, 1, currPower[index])
                 index += 1
            print ("Max Powers Set: ", currPower)
            print ("Total Power: ", sum(currPower))
            end = datetime.datetime.now()
            print("End:", end)

            # Sleep 5 Minutes, Then Repeat
            time.sleep(60*5)
            print ("")
