from game import Game
import time


def main():
    game = Game()
    # game.start()
    start = time.time()
    game.solve()
    end = time.time()
    print(f"Program worked for {end - start} seconds")


if __name__ == "__main__":
    main()
