import requests
import typing
import socket


BASE_URL = "http://missiledefense.ddns.net"
POST_ENDPOINT = "/api/addscore/"
GET_ENDPOINT = "/api/highscores/"
REMOTE_SERVER = "www.google.com"


def parse_high_scores(payload):
	list_of_scores = payload["scores"]
	parsed_scores = []
	for score in list_of_scores:
		parsed_scores.append((score["name"], score["score"]))
	return parsed_scores


def post_new_score(name: str, score: int) -> None:
	json_to_send = {"name": name, "score": score}
	resp = requests.post(f"{BASE_URL}{POST_ENDPOINT}", json=json_to_send)
	resp.raise_for_status()


def get_high_scores() -> typing.List[typing.Tuple[str, int]]:
	resp = requests.get(f"{BASE_URL}{GET_ENDPOINT}")
	resp.raise_for_status()
	return parse_high_scores(resp.json())


def is_connected():
	try:
		host = socket.gethostbyname(REMOTE_SERVER)
		s = socket.create_connection((host, 80), 2)
		s.close()
		return True
	except:
		pass
	return False
