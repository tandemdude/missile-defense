from concurrent import futures
import requests
import typing
import time


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


class APIWorker:
    def __init__(self):
        self.executor = futures.ThreadPoolExecutor(max_workers=2)

    def _post_score(self, name: str, score: int) -> None:
        """
        Sends a POST request to the api endpoint to register
        a new score into the global high scores database

        :param name: :class:`str` name to be stored
        :param score: :class:`int` score to be stored
        :return: `None`
        """
        try:
            json_to_send = {"name": name, "score": score}
            resp = requests.post(f"{BASE_URL}{POST_ENDPOINT}", json=json_to_send)
            resp.raise_for_status()
        except:
            pass

    def _get_scores(self) -> typing.List[typing.Tuple[str, int]]:
        """
        Sends a GET request to the api endpoint to fetch the
        top 10 highest scores from the global high score database

        :return: :class:`list` of name, score pairs
        """
        try:
            resp = requests.get(f"{BASE_URL}{GET_ENDPOINT}", timeout=5)
            resp.raise_for_status()
            response = resp.json()
        except:
            response = "FAILED"
        finally:
            return response

    def post_score(self, name, score):
        return self.executor.submit(self._post_score, name, score)

    def get_scores(self):
        return self.executor.submit(self._get_scores)
