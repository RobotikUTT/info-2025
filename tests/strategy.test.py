from modules.strategy.structure_validator import verify
from utils.config import Config

def main():
    strategy = Config().get()["strategy"]["path"]
    verify(strategy)

if __name__ == "__main__":
    main()