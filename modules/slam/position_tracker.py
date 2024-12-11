class PositionTracker:
    _instance = None

    def __new__(cls):
        # Check if an instance already exists
        if cls._instance is None:
            # If not, create it
            cls._instance = super(PositionTracker, cls).__new__(cls)
        # Return the existing or newly created instance
        return cls._instance

    def __init__(self):
        # Ensure the initialization is done only once
        if not hasattr(self, 'initialized'):
            self.position = (0, 0, 0)  # Initialize position
            self.initialized = True

    def getCurrentPosition(self):
        return self.position

    def setCurrentPosition(self, position):
        self.position = position
