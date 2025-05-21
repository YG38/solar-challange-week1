"""Basic test file to verify the testing setup."""

def test_import():
    """Test that the package can be imported."""
    import src  # noqa: F401
    assert True

def test_always_passes():
    """Sample test that always passes."""
    assert True
