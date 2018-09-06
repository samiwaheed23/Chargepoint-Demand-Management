# Chargepoint-Demand-Management
##### Author: Sami Waheed
##### Date: September 2018

## Description:
This program accesses Chargepoint's API for demand management calls. This is only a class definition that contains helpful functions to proceed with controlling the power sent to Chargepoint's electric vehicle charging stations. I used this to conduct smart charging for a private group of charging stations at a site. For security purposes I have not included the algorithm or any techniques utilized, so any further  implementations will need to be written according to the user's needs. Each charging station this code was used for had 2 individual ports attached and there were instances where each port needed to be dealt with separately. Also, this approach utilized the Zeep Client to make requests to the SOAP API.

## Note: 
Any demand management API call requires having Chargepoint's highest service plan, or else an error will be thrown upon making the call. You also have to use the API keys given to an "API User" account.

## Helpful Links:
1. Chargepoint SOAP API 5.0: https://na.chargepoint.com/programmers_guide/5.0
2. Zeep Client Install Guide: https://python-zeep.readthedocs.io/en/master/

## Files:
1. CP_levelload.py
