import requests
import typing
import socket


BASE_URL = "http://missiledefense.ddns.net"
POST_ENDPOINT = "/api/addscore/"
GET_ENDPOINT = "/api/highscores/"
REMOTE_SERVER = "www.google.com"


def parse_high_scores(payload) -> typing.List[typing.Tuple[str, int]]:
    """
    Takes a json payload and converts it into a list of tuples
    expected by the :class:`source.highscore.HighscoreTable` to
    generate the rows with

    :param payload: :class:`dict` containing name and score data
    :return: :class:`list` of name, score pairs
    """
    list_of_scores = payload["scores"]
    parsed_scores = []
    for score in list_of_scores:
        parsed_scores.append((score["name"], score["score"]))
    return parsed_scores


def post_new_score(name: str, score: int) -> None:
    """
    Sends a POST request to the api endpoint to register
    a new score into the global high scores database

    :param name: :class:`str` name to be stored
    :param score: :class:`int` score to be stored
    :return: `None`
    """
    json_to_send = {"name": name, "score": score}
    resp = requests.post(f"{BASE_URL}{POST_ENDPOINT}", json=json_to_send)
    resp.raise_for_status()


def get_high_scores() -> typing.List[typing.Tuple[str, int]]:
    """
    Sends a GET request to the api endpoint to fetch the
    top 10 highest scores from the global high score database

    :return: :class:`list` of name, score pairs
    """
    resp = requests.get(f"{BASE_URL}{GET_ENDPOINT}")
    resp.raise_for_status()
    return parse_high_scores(resp.json())


def is_connected() -> bool:
    """
    Attempts to open a websocket connection to google's servers in order
    to find out whether or not the computer is connected to the internet

    :return: :class:`bool` indicating whether or not the computer is connected to the internet
    """
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False
