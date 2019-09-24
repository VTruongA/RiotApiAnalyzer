import requests
import time

class summoner:

    def __init__(self,name,summonerID, accountID):
        self._name = name
        self._summonerID = summonerID
        self._accountID = accountID

    def get_name(self):
        return self._name

    def get_summonerID(self):
        return self._summonerID

    def get_accountID(self):
        return self._accountID


def main():
    region = "na"
    summonerName = "Cute Raichu"
    APIKey = "RGAPI-95bd6407-a1ef-4e4b-ac87-9f39d38e23d4"
    
    summonerJson = requestData(region, summonerName, APIKey)
    currentSum = summoner(summonerJson['name'],summonerJson['id'],summonerJson['accountId'])

    ddragonJson = requestddragon()

    #only ranked matches right now
    matches = requestMatch(region, currentSum.get_accountID(), APIKey, ddragonJson,currentSum.get_name())
    print(matches)

def userInput(APIKey):
    '''
    Input function, takes in apikey but ask for summoner names and region. need to think of a way
    to compare data with the request matches function
    '''
    summonerNames = input("Type in all the summoner names seperated by a comma ','")
    region = input("Type in the region. Ex. 'na'")
    summonerNames = summonerNames.split(',')
    returnList = []
    for names in summonerNames:
        summonerJSON = requestData(region, names, APIKey)
        returnList.append(summoner(summonerJSON['name'),summonerJSON['id'],summonerJSON['accountId'])
    return returnList

def requestData(region, summonerName, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
          summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestddragon():
    URL = "http://ddragon.leagueoflegends.com/cdn/9.18.1/data/en_US/champion.json"
    response = requests.get(URL)
    return response.json()

def requestMatch(region, accountID, APIKey, ddragonJson,name):
    #dictionary of champs played and K/D/A + TotalGames
    champPlayed = {'numOfGames':0}
    #only ranked, 20 games starting from 9/17
    URL = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/"+ accountID + "?queue=420&beginTime=1568196000&endIndex=20&api_key=" + APIKey
    response = requests.get(URL).json()
    #with the match list, turns the championID into the acutal name
    champIdTranslator(region,accountID,response, ddragonJson)
    #starts to build up the dictionary by going into each game given by the match list
    parseChamps(response,champPlayed, APIKey, name)

    return champPlayed


def champIdTranslator(region,accountID, matchesJSON, championJSON):
    "translate the championID into the champion's name"
    #print(championJSON)
    id2ChampDict = {}
    for champion in championJSON['data']:
        id2ChampDict[int(championJSON['data'][champion]['key'])] = championJSON['data'][champion]['id']

    # id2ChampDict is now key: id, value: champion name
    for match in matchesJSON['matches']:
        champ_id = match['champion']
        match['champion'] = id2ChampDict[champ_id]

def parseChamps(matchList,champPlayed, APIKey, name ):
    '''With the match list, the player's games will be seperated based on
    champion'''
    for games in matchList["matches"]: #goes through each game in the player's match list
        if games['champion'] not in champPlayed: #if a champion hasn't been played yet, then it will be added to the dictionary
            champPlayed[games['champion']] = {'totalK':0,'totalD':0,'totalA':0,"totalGames":0}
        currGameStats = basicStats(games['gameId'], APIKey, name, games['champion'],champPlayed) #adds the stats from this game into the respective champion's value
    

def basicStats(gameId, APIKey, name, champName, champPlayed):
    '''calculate the avg stats of each champion'''
    URL = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(gameId) + "?api_key=" + APIKey
    response = requests.get(URL).json()
    for  participants in response['participantIdentities']: #finds what the selected summoner's number is in this game
        if participants["player"]["summonerName"] == name:
                particNum = participants["participantId"] - 1
                
    currentStats = response["participants"][particNum] #goes to the selected summoner's section of stats
    champPlayed[champName]['totalK'] = champPlayed[champName]['totalK'] + currentStats['stats']["kills"]    #add kills
    champPlayed[champName]['totalD'] = champPlayed[champName]['totalD'] + currentStats['stats']["deaths"]   #adds deaths
    champPlayed[champName]['totalA'] = champPlayed[champName]['totalA'] + currentStats['stats']["assists"]  #adds assists
    champPlayed[champName]['totalGames'] = champPlayed[champName]['totalGames'] + 1                         #adds total games on that champ
    champPlayed['numOfGames'] = champPlayed['numOfGames'] + 1                                               #adds to the amount of games that has been played since starting date

main()

'''
   Author: Vincent Truong, Riley Simpson, David Grozier
   Last Updated: 9/23/2019
'''
