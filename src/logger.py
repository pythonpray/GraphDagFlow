import logging


def setup_logger(level, logger_name="graph_dag_flow"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


root_logger = setup_logger("INFO")
