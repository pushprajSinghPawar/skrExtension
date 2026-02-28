import logging

logging.basicConfig(
    filename="secura.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def log(msg):
    """Helper wrapper around logging.info so other modules can import it."""
    logging.info(msg)
