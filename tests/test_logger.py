from dataquantum_logger.logger import setup_logger


def test_setup_logger() -> None:
    """Test the function return value."""
    result = setup_logger("DataQuantum")

    assert result == "DataQuantum"
