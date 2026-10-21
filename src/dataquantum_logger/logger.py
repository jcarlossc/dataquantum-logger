import logging
from pathlib import Path
from typing import Any


def setup_logger(
    logging_config: dict[str, Any],
    show_console: bool = False,
) -> None:
    """
    Configure logging to a file and optionally to the console.

    Parameters
    ----------
    logging_config : dict[str, Any]
        Dictionary containing the logging and logs configurations.
        Required keys are logging.level, logging.format,
        logging.encoding and logs.file.
    show_console : bool, default=False
        If True, display log messages in the console.
        If False, write logs to the file only.

    Returns
    -------
    None
        Configure the root logger without returning a value.

    Raises
    ------
    ValueError
        If the configuration is missing required keys or has invalid types.
    OSError
        If the log directory or file cannot be created or opened.

    Notes
    -----
    The function uses logging.basicConfig with force=True.
    Existing handlers on the root logger are replaced.
    """

    logger = logging.getLogger(__name__)

    try:
        # Ensures that the folder exists.
        Path(logging_config["logs"]["file"]).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Gets the logging level defined in the configuration.
        # If the level does not exist, it uses INFO as the default.
        level = getattr(
            logging,
            logging_config["logging"]["level"],
            logging.INFO,
        )

        # Always write logs to a file.
        handlers: list[logging.Handler] = [
            logging.FileHandler(
                logging_config["logs"]["file"],
                encoding=logging_config["logging"]["encoding"],
            ),
        ]

        # Add console output only when explicitly requested.
        if show_console:
            handlers.append(logging.StreamHandler())

        # Configure the root logger with the selected handlers.
        logging.basicConfig(
            level=level,
            format=logging_config["logging"]["format"],
            handlers=handlers,
            force=True,
        )

        logger.info("Logger configurado com sucesso.")

    except (KeyError, TypeError) as error:
        # Provide a consistent error message for invalid configurations.
        raise ValueError(f"CONFIG_ERROR: invalid configuration -> {error}") from error

    except OSError as error:
        # Preserve the original filesystem error as the exception cause.
        raise OSError(
            f"FILE_ERROR: error in the log file.'{logging_config}' -> {error}"
        ) from error
