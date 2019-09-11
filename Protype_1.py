import requests
import time

def main():
    #region = input('What region? ').upper()
    #summonerName = input("What's your summoner name? ")
    #APIKey = input("Paste the API key: ")
    region = "na"
    summonerName = "Cute Raichu"
    APIKey = "RGAPI-74765c03-82e0-4bfa-a0e0-945c8f45cd12"
    jsonFile = requestData(region, summonerName, APIKey)
    print(jsonFile)
    matches = requestMatch(region, jsonFile["accountId"], APIKey)
    print()
    print(matches)

def requestData(region, summonerName, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
          summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatch(region, accountID, APIKey):
    #fromWhen = input("From what date do you want to begin the match list? MM/DD/YYYY")
    #toWhen = input("To what date do you want to begin the match list? MM/DD/YYYY")
    
    fromWhen,toWhen = "09/10/2019","09/11/2019"
    pattern = "%m/%d/%Y"
    beginTime = str(time.mktime(time.strptime(fromWhen, pattern))) * 1000
    endTime = int(time.mktime(time.strptime(toWhen, pattern))) * 1000
    URL = "https://" + region + "1.api.riotgames.com/lol/match/v4/matchlists/by-account/"+ accountID +"?beginTime=1568098800000&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

main()
