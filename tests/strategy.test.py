from modules.strategy.structure_validator import verify
from utils.config import Config
# TODO : ❌ Erreur de validation : 'configuration/strategy.yml' is not of type 'array'
def main():
    strategy = Config().get()["strategy"]["path"]
    verify(strategy)

if __name__ == "__main__":
    main()