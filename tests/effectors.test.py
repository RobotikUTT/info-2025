from modules.effectors.effectors_control import EffectorsControl
import time


def main():
    eff = EffectorsControl("esp_effectors") #string de l'i2c mapping
    eff.set_banner_close()
    time.sleep(3)
    eff.set_banner_open()
    time.sleep(3)
    eff.take_everything()
    time.sleep(3)
    eff.put_down_everything()
    time.sleep(3)


if __name__ == "__main__":
    main()
