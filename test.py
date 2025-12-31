from csv import writer, reader

with open("highscores.csv", "w") as fl:
    w = writer(fl, lineterminator="\n")
    w.writerows([["0", "___"], ["0", "FAB"]])

with open("highscores.csv", "r") as fl:
    print(list(reader(fl)))