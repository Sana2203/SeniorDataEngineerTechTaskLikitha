from unittest.mock import Mock, patch
import pytest
from etl_pipeline.api_client import fetch_json


def test_fetch_json_returns_list():
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "title": "Hello"}]
    mock_response.raise_for_status.return_value = None

    with patch("etl_pipeline.api_client.requests.get", return_value=mock_response):
        result = fetch_json("https://example.com/posts")

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_fetch_json_raises_for_non_list():
    mock_response = Mock()
    mock_response.json.return_value = {"error": "unexpected"}
    mock_response.raise_for_status.return_value = None

    with patch("etl_pipeline.api_client.requests.get", return_value=mock_response):
        with pytest.raises(ValueError):
            fetch_json("https://example.com/posts")