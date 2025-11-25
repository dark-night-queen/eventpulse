# Standard Library imports
import signal
import time
from loguru import logger


class BaseWorker:
    """
    Base class that handles:
      - SIGINT / SIGTERM shutdown
      - running loop
      - lifecycle logging
    """

    poll_interval: float = 0.1

    def __init__(self):
        logger.info(f"Initializing {self.__class__.__name__}...")

        self.running = True
        self.register_signal_handlers()

    # ---------------------------
    # Signal handling
    # ---------------------------
    def register_signal_handlers(self):
        logger.info("Registering signal handlers...")

        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def handle_shutdown(self, sig, frame):
        logger.warning(f"Received signal {sig}, shutting down gracefully...")
        self.running = False

    # ---------------------------
    # Template methods
    # ---------------------------
    def setup(self):
        """Optional setup hook for child classes."""
        pass

    def process(self):
        """Child class implements this."""
        raise NotImplementedError("process() must be implemented by subclass")

    def cleanup(self):
        """Optional cleanup hook for child classes."""
        pass

    # ---------------------------
    # Worker lifecycle
    # ---------------------------
    def run(self):
        logger.info(f"Starting worker: {self.__class__.__name__}")
        self.setup()

        try:
            while self.running:
                self.process()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            logger.warning("Keyboard interrupt received.")
        finally:
            self.cleanup()
            logger.info(f"Worker stopped: {self.__class__.__name__}")
