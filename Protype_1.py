import requests
import time

def main():
    #region = input('What region? ').upper()
    #summonerName = input("What's your summoner name? ")
    #APIKey = input("Paste the API key: ")
    region = "na"
    summonerName = "Cute Raichu"
    APIKey = ""
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

def numToEnglish(region,accountID, APIKey):
    "translate the championID into the champion's name"
    continue

def parseChamps(region,accountID,APIKey,matches):
    '''With the match list, the player's games will be seperated based on
    champion'''
    continue

def basicStats(region, accountID, APIKey):
    '''calculate the avg stats of each champion'''
    continue

def statsWithDuo(region, accountID, APIKey):
    '''If the selected summoner plays with another player constantly,
        it'll keep track of what their stats are like together.'''
    continue

def firstBlood(region, accountID, APIKey):
    ''' '''
    continue
main()

'''
   Author: Vincent Truong
   Collaborators: David Grozier
   Start Date: 9/6/2019
   Last Updated: 9/16/2019
'''
