from flask import Flask, request
import json
import sys
import datetime
app = Flask(__name__)

###Gather and setup data
overallMap ={}
file= open("data.txt", encoding="utf8") 
for line in file:
    line = line.strip()
    if not line: continue

    if line.startswith('Teams') or line.startswith('Players') or line.startswith('Games') or line.startswith('Player Stats') or line.startswith('Game State'):
        if line not in overallMap:
          overallMap[line[:-1].lower()] = []
        heading = line[:-1].lower()
        continue
    if line[-1] == ",": line = line[:-1]
    lineMap = json.loads(line)
    overallMap[heading].append(lineMap) 


 
def formatDate(dataDate): 
  splitDate = dataDate.split("/")
  formedDate = ""
  
  for x in splitDate:
    tmp = x
    if int(tmp) < 10:
      tmp = '0' + tmp
  
    formedDate += tmp
  
  return formedDate

@app.route('/nba/teams')
def getTeams():
  tempList = overallMap.get("teams")
  jsonReturnArray = json.dumps(tempList, sort_keys=True, indent = 4)
  
  return jsonReturnArray

@app.route('/nba/teams/<id>')
def getTeamById(id):
  jsonTeam = {}
  teamsList = overallMap.get("teams")
  
  for team in teamsList:
    tmpTeamId = team.get("id")
    if str(tmpTeamId) == id:
        jsonTeam = json.dumps(team, sort_keys=True, indent = 4)
        break
  
  return jsonTeam
  
@app.route('/nba/players')
def getPlayers():
  
  passedInDate = request.args.get("date", None)
  
  if passedInDate!= None:
    
    foundGame = ""

    gameList = overallMap.get("games")
    statsList = overallMap.get("player stats")
    playersList = overallMap.get("players")
    gameStateList = overallMap.get("game state")
    
    foundGameList = []
    for game in gameList:
      gameDate = formatDate(game.get("date"))
      
      if passedInDate == gameDate:
        foundGameList.append(game.get("id"))

    foundStatsList = []
    print(foundGameList)
    for stat in statsList:
      if stat.get("game_id") in foundGameList:
        foundStatsList.append(stat.get("player_id"))

    foundPlayersList = []
    for player in playersList :
      if player.get("id") in foundStatsList:
        foundPlayersList.append(player)
    
    jsonReturnArray = json.dumps(foundPlayersList, sort_keys=True, indent = 4)
    
    
    return jsonReturnArray
  
  tempList = overallMap.get("players")
  jsonReturnArray = json.dumps(tempList, sort_keys=True, indent = 4)
  
  return jsonReturnArray
 
 
@app.route('/nba/players/<id>')
def getPlayerById(id):
  jsonPlayer = {}
  playersList = overallMap.get("players")
  
  for player in playersList:
    tmpPlayerId = player.get("id")
    print(tmpPlayerId, file=sys.stdout)
    print(player, file=sys.stdout)
    if str(tmpPlayerId) == id:
        jsonPlayer = json.dumps(player, sort_keys=True, indent = 4)
        break
  
  return jsonPlayer

@app.route('/nba/players/<id>/stats')
def getPlayerStats(id):
  jsonStatsArray = []
  statsList = overallMap.get("player stats")
  
  for stat in statsList:
    statPlayerId = stat.get("player_id")
    if str(statPlayerId) == id:
      jsonStatsArray.append(stat)
    
  jsonStat = json.dumps(jsonStatsArray, sort_keys=True, indent = 4)
  
  return jsonStat
  

@app.route('/nba/games')
def getGames():
  gameList = overallMap.get("games")
  gameStateList = overallMap.get("game state")
  
  passedInDate = request.args.get("date", None)
  
  if passedInDate!= None:
    tmpMap = {}
    finalGamesList = []
    foundGameList = []
    for game in gameList:
      gameDate = formatDate(game.get("date"))
      if passedInDate == gameDate:
        foundGameList.append(game)
        

    for game in foundGameList:
      for gameState in gameStateList:
        if game.get("id") == gameState.get("game_id"):
          tmpMap = game
          tmpMap["gameState"] = gameState
          finalGamesList.append(tmpMap)

    
    
    jsonReturnArray = json.dumps(finalGamesList, sort_keys=True, indent = 4)
    
    
    return jsonReturnArray
    
  tmpMap = {}
  finalGamesList = []
  for game in gameList:
    for gameState in gameStateList:
      if game.get("id") == gameState.get("game_id"):
        tmpMap = game
        tmpMap["gameState"] = gameState
        finalGamesList.append(tmpMap)
      
  jsonGame = json.dumps(finalGamesList, sort_keys=True, indent = 4)
  
  return jsonGame
  
  
@app.route('/nba/games/<id>')
def getGameByID(id):
  gameList = overallMap.get("games")
  gameStateList = overallMap.get("game state")
  foundGameMap = {}
  finalGamesList = []
  for game in gameList:
    for gameState in gameStateList:
      if int(id) == game.get("id") == gameState.get("game_id"):
        foundGameMap = game
        foundGameMap["gameState"] = gameState
        break
      
    
  
  jsonGame = json.dumps(foundGameMap, sort_keys=True, indent = 4)
  
  return jsonGame


