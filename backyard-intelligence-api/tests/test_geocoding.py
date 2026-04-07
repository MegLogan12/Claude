import pytest

from app.providers.google_provider import GoogleGeocodingProvider
from app.utils.validation import is_valid_us_address


@pytest.mark.asyncio
async def test_geocoding_stub_flow() -> None:
    provider = GoogleGeocodingProvider(api_key="")
    result = await provider.geocode("123 Main St, Dallas, TX 75201")
    assert result["provider"] == "stub"
    assert "latitude" in result


def test_address_validation() -> None:
    assert is_valid_us_address("123 Main St, Dallas, TX 75201")
    assert not is_valid_us_address("Main Street Dallas")
