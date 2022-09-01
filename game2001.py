import random
from flask import Flask, request

app = Flask(__name__)


HTML_START = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess The Number</title>
</head>
<body>
<h1>User [0] vs Computer [0]</h1>
<form action="" method="POST">
    <input type="hidden" name="points_player1" value="{}">
    <input type="hidden" name="points_player2" value="{}">
    <input type="submit" value="ROLL DICES">
</form>
</body>
</html>
"""

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>2001 game</title>
</head>
<body>
<h1>User [{points_player1}] vs Computer [{points_player2}]</h1>
<form action="" method="POST">
    <input type="hidden" name="points_player1" value="{points_player1}">
    <input type="hidden" name="points_player2" value="{points_player2}">
    <input type="submit" value="KEEP ROLLING DICES">
</form>
</body>
</html>
"""

HTML_FINISH = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>2001 game</title>
</head>
<body>
<h1>User [{points_player1}] vs Computer [{points_player2}]</h1>
<form action="" method="GET">
    <input type="submit" value="Play again">
</form>
</body>
</html>
"""

def roll_the_dice_x2():
    """sum of points for throwing a dice twice"""
    return random.randint(1, 6) + random.randint(1, 6) 

def calculate_points(points):
    """calculating points after throwing dices -special rules apply"""
    roll = roll_the_dice_x2()
    if roll == 7:
        points //= 7
    elif roll == 11:
        points *= 11
    else:
        points += roll
    
    return points

@app.route("/", methods=["GET", "POST"])
def game_2001():
    """The main function for the game"""
    if request.method == "GET":
        return HTML_START.format(0, 0)
    else:
        points_player1 = int(request.form.get("points_player1")) # reads points from the HTML form
        points_player2 = int(request.form.get("points_player2")) # reads points from the HTML form
        points_player1 += calculate_points(points_player1)       # calculate points after throwing dices
        points_player2 += calculate_points(points_player2)       # calculate points after throwing dices
        
        while points_player1<2001 and points_player2<2001:       # if neither of the players reach 2001 points, the game continues
            return HTML.format(points_player1=points_player1, points_player2=points_player2)
        
        if points_player1>points_player2:
            return HTML_FINISH.format(points_player1="WIN", points_player2="LOST")
        elif points_player1<points_player2:
            return HTML_FINISH.format(points_player2="WIN", points_player1="LOST")
        else:
            return HTML_FINISH.format(points_player2="DRAW", points_player1="DRAW")

if __name__ == '__main__':
    app.run()
