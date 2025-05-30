from modules.strategy.structure_validator import verify
from utils.config import Config
import yaml
# TODO : ❌ Erreur de validation : 'configuration/strategy.yml' is not of type 'array'
def main():
    with open(Config().get()["strategy"]["path"]) as f:
        data = yaml.safe_load(f)
        print("Type YAML chargé :", type(data))
        verify(data)

if __name__ == "__main__":
    main()