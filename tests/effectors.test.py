from modules.effectors.effectors_control import EffectorsControl
import time


def main():
    eff = EffectorsControl()
    while True:
        for i in range(4):
            eff.magnetize(i)
        time.sleep(3)
        for i in range(4):
            eff.demagnetize(i)
        time.sleep(3)


if __name__ == "__main__":
    main()
