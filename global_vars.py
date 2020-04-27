import hider

screen_width = 200
screen_height = 200


def spawn_hider():
	return hider.hider(50, (screen_height / 2) - 10, 20, 20, (0,255,0))