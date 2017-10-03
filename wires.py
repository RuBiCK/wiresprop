import time

combinations = [[1, 2], [3, 4], [5, 6]]
gpiosUsed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
wires = len(combinations)
correctCombinations = 0


def setInputGpios(gpiolist):
    # TODO set to input gpiosUsed
    pass


def checkPairStatus(pair):
    src = pair.pop()
    # TODO set SRC GPIO to output and set 1
    dst = pair.pop()

    # Check
    if dst == 1:
        correctCombinations += 1

    # TODO: Set src and dst to input
    return


def playEnd():
    pass


def main():
    while correctCombinations < wires:
        correctCombinations = 0
        setInputGpios()
        for pair in combinations:
            checkPairStatus(pair)

    time.sleep(0.2)
    playEnd()
    # TODO:Only play once. Wait for a button pressed


if __name__ == "__main__":
    main()
