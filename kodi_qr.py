import yaml
import requests
import os
import itertools

if(not os.path.isfile('credentials.yaml')):
    username = input("Enter kodi username: ")
    password = input("Enter kodi password: ")
    credentials = {"username" : username, "password" : password}
    with open('credentials.yaml', 'w') as file:
        yaml.dump(credentials, FileExistsError)

with open('credentials.yaml', 'r') as file:
    credentials = yaml.load(file, Loader=yaml.FullLoader)

message_id_counter = itertools.count()

def get_movie_id_from_title(title, username, password, message_id_counter):
    response = requests.post('http://localhost:8080/jsonrpc',
        json={"jsonrpc": "2.0", 
            "method": "VideoLibrary.GetMovies", 
            "id": next(message_id_counter),
            "params": {"filter":
                {"field": "title",
                "operator": "is",
                "value": title}}},
        timeout=5,
        auth=(username, password))
    response.raise_for_status()
    return(response.json()["result"]["movies"][0]["movieid"])

def play_movie_from_title(title, username, password, message_id_counter):
    response = requests.post('http://localhost:8080/jsonrpc',
        json={"jsonrpc": "2.0", 
            "method": "Player.Open",
            "id": next(message_id_counter),
            "params": {"item":{"movieid": get_movie_id_from_title(title, 
                username,
                password, 
                message_id_counter)}}},
        timeout=5,
        auth=(username, password))
    response.raise_for_status()
    return(response)

def stop_all_players(username, password, message_id_counter):
    active_players = requests.post('http://localhost:8080/jsonrpc',
        json={"jsonrpc": "2.0",
            "method": "Player.GetActivePlayers",
            "id": next(message_id_counter)}, 
        timeout=5,
        auth=(username,password))
    responses={}
    for i in active_players.json()["result"]:
        responses[i["playerid"]] = requests.post('http://localhost:8080/jsonrpc',
            json={"jsonrpc": "2.0", 
                "method": "Player.Stop",
                "params": {"playerid" : i["playerid"]},
                "id": next(message_id_counter)}, 
            timeout=5,
            auth=(username, password))
    for i in responses:
        i.raise_for_status()
    return(responses)

def play_pause(username, password, message_id_counter):
    active_players = requests.post('http://localhost:8080/jsonrpc',
        json={"jsonrpc": "2.0",
            "method": "Player.GetActivePlayers",
            "id": next(message_id_counter)}, 
        timeout=5,
        auth=(username,password))
    if(len(active_players.json()["result"]) > 0):
        response = requests.post('http://localhost:8080/jsonrpc',
            json={"jsonrpc": "2.0", 
                "method": "Player.PlayPause",
                "params": {"playerid" : active_players.json()["result"][0]["playerid"]},
                "id": next(message_id_counter)}, 
            timeout=5,
            auth=(username, password))
        response.raise_for_status()
        return(response)
    else:
        return(False)

def get_movie_data(username, password, message_id_counter):
    response = requests.post('http://localhost:8080/jsonrpc',
        json={"jsonrpc": "2.0", 
            "method": "VideoLibrary.GetMovies", 
            "id": next(message_id_counter),
            "params": {"properties" : ["thumbnail", "playcount", "file"], 
            "sort": { "order": "ascending", 
                    "method": "label", 
                    "ignorearticle": True }}},
        timeout=5,
        auth=(username, config))
    response.raise_for_status()
    return(response.json()["result"]["movies"])