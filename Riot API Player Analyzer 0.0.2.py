import requests
import time

def main():
    region = "na"
    summonerName = "Cute Raichu"
    APIKey = ""
    
    summonerJson = requestData(region, summonerName, APIKey)
    currentSum = summoner(summonerJson['name'],summonerJson['id'],summonerJson['accountId'])

    ddragonJson = requestddragon()

    #only ranked matches right now
    matches = requestMatch(region, currentSum.get_accountID(), APIKey, ddragonJson,currentSum.get_name())

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

def champIdTranslator(region,accountID, APIKey, matchesJSON):
    "translate the championID into the champion's name"
    championJSON = requests.get("http://ddragon.leagueoflegends.com/cdn/9.18.1/data/en_US/champion.json").json()
    
    # establishes a new dict and creates pairs ex: {111: 'Nautilus'}
    id2ChampDict = {}
    for champion in championJSON['data']:
        id2ChampDict[int(championJSON['data'][champion]['key'])] = championJSON['data'][champion]['id']

    # updates the 'champion' value in the match JSON with a string name ex: 'Aatrox'
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

def statsWithDuo(region, accountID, APIKey):
    '''If the selected summoner plays with another player constantly,
        it'll keep track of what their stats are like together.'''
    pass

def firstBlood(region, accountID, APIKey):
    ''' '''
    pass

main()

'''
   Author: Vincent Truong
   Collaborators: David Grozier, Riley Simpson
   Start Date: 9/6/2019
   Last Updated: 9/16/2019
'''
