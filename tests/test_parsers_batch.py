import pytest
import json
from siyarix.parsers import ParserRegistry

@pytest.fixture(scope="module")
def registry():
    reg = ParserRegistry()
    reg.discover()
    return reg

def test_registry_discovery(registry):
    tools = registry.registered_tools()
    assert len(tools) > 0, "Should have discovered parsers"

def test_all_parsers_safe_parse_empty(registry):
    """Test all discovered parsers with empty string to ensure they handle it."""
    for tool in registry.registered_tools():
        res = registry.parse(tool, "")
        assert isinstance(res, list), f"{tool} parser did not return a list for empty input"

def test_all_parsers_safe_parse_plaintext(registry):
    """Test all discovered parsers with garbage plaintext."""
    plaintext = "This is not valid JSON or expected command output.\n" * 10
    for tool in registry.registered_tools():
        res = registry.parse(tool, plaintext)
        assert isinstance(res, list), f"{tool} parser did not return a list for plaintext"

def test_all_parsers_safe_parse_json(registry):
    """Test all discovered parsers with unexpected JSON."""
    bad_json = json.dumps({"unrelated": "data", "status": "failed"})
    bad_json_list = json.dumps([{"fake": "array"}])
    
    for tool in registry.registered_tools():
        res1 = registry.parse(tool, bad_json)
        assert isinstance(res1, list)
        
        res2 = registry.parse(tool, bad_json_list)
        assert isinstance(res2, list)

def test_registry_methods(registry):
    assert registry.has_parser("nmap") is True
    assert registry.has_parser("nonexistent_tool") is False
    assert registry.count > 0
    assert registry.get("nmap") is not None
    assert registry.get("nonexistent_tool") is None
