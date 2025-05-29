# info-2025

### Architecture

```
info-2025/
│
├── main.py                      # Main application entry point
├── config.yml                   # Config for I2C, logger and so on
├── data/                        # Folder containing data logs from application runs
├── modules/                     # Brain of the program, containing all resources
│   ├── actions/                 # Classes to realize robots actions
│   ├── communication/           # Classes for I2C communication
│   ├── gui/                     # Classes for GUI management and interaction
│   ├── navigation/              # Classes to manage navigation (from point A to point B by which strategy ie straight, follow a line/a wall)
│   ├── slam/                    # Simultaneous localization and mapping : classes to manage the current position and obstacles
│   └── template.py              # Template class for a module object
├── utils/                       # Useful functions
│   ├── config.py                # Config class to avoid passing config as parameter for each class object
│   ├── tools.py                 # Tooling functions
│   └── log.py                   # Custom logging class
├── strategies/                  # Strategies in YAML format to facilitate non developper customization
│   └── default.yml
├── simulations/                 # Folder containing script to simulate ESP interactions for debugging
│   ├── re_run.py                # Allows to re run the application from previosu data logged (to avoid crashing real robot 3 times for debug)
│   └── esp_runner.py            # Simulate ESP32 communications
├── tests/                       # Unit tests for the application
│   └── test_template.py
└── requirements.txt             # Project dependencies

```

### Installation

Install necessary requirements :

```bash
sudo apt install build-essential libsystemd-dev \
  && curl -LsSf https://astral.sh/uv/install.sh | sh \
  && uv sync
```

Enable I2C on Raspberry :

```bash
sudo raspi-config
# Interfaces
# Enable I2C for esp com
# Enable serial, without enabling shell for the lidar
```

Set up the config.yml file.

To install all libs needed without keeping temp artefacts :

```bash
uv venv # to create the virtual env
uv pip install -e .
```

Then run :

```bash
uv run main.py
```

### Développement

Pour formatter et linter le code :

```bash
uv run ruff check
uv run ruff format
```

##### Modules

Chaque classe de module doit être créé à partir de `template.py` afin d'initialiser le logger et la
config.

##### Logging

Après avoir initialisé le logger comme suit en spécifiant le nom de la classe actuelle :
`log = Log("TestPlugin")`

On peut utiliser ces 4 méthodes :

```python
log.info("info message")
log.debug("debug message")
log.warn("warning message")
log.error("error message", Exception)
```
