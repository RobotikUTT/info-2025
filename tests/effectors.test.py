from modules.effectors.effectors_control import EffectorsControl
import time


def main():
    eff = EffectorsControl()
    eff.set_banner_close()
    time.sleep(300)
    eff.set_banner_open()
    time.sleep(300)
    eff.take_everything()
    time.sleep(300)
    eff.put_down_everything()
    time.sleep(300)


if __name__ == "__main__":
    main()
