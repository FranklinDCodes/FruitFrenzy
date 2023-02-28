from game import Game

g = Game()
g.launch_game()
while g.running:
    g.main_loop()
