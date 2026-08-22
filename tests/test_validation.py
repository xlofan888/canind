from src.validation.values import validate_range
import pytest

def test_unemployment_range(): assert validate_range('unemployment',6.4)
def test_unemployment_invalid():
 with pytest.raises(ValueError): validate_range('unemployment',101)
