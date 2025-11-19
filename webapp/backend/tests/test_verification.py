"""Test game verification - TDD approach

RED: Write failing test first
GREEN: Make it pass with minimal code
REFACTOR: Clean up if needed
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.verify_service import GameVerificationService, VerificationResult


class TestGameVerification:
    """Test game verification catches common issues"""

    @pytest.mark.asyncio
    async def test_detects_console_errors(self):
        """Test that verification detects JavaScript console errors"""
        # Arrange: HTML with JavaScript error
        broken_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Broken Game</title></head>
        <body>
            <h1>Test Game</h1>
            <button id="start">Start</button>
            <script>
                // This will cause a console error
                undefinedFunction();
            </script>
        </body>
        </html>
        """

        # Act: Run verification
        verifier = GameVerificationService()
        result = await verifier.verify_game("test-project-id", broken_html)

        # Assert: Should detect the error
        assert result.passed == False, "Should fail for games with console errors"
        assert len(result.errors) > 0, "Should have error messages"
        assert any("undefinedFunction" in err or "not defined" in err for err in result.errors), \
            "Should detect undefined function error"

    @pytest.mark.asyncio
    async def test_passes_working_game(self):
        """Test that verification passes for working games"""
        # Arrange: Working HTML
        working_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Working Game</title></head>
        <body>
            <h1>Test Game</h1>
            <button id="start">Start</button>
            <canvas id="game"></canvas>
            <script>
                document.getElementById('start').addEventListener('click', function() {
                    console.log('Game started');
                });
            </script>
        </body>
        </html>
        """

        # Act: Run verification
        verifier = GameVerificationService()
        result = await verifier.verify_game("test-project-id", working_html)

        # Assert: Should pass
        assert result.passed == True, "Should pass for working games"
        assert len(result.errors) == 0, "Should have no errors"

    @pytest.mark.asyncio
    async def test_detects_missing_interactive_elements(self):
        """Test that verification detects games with no interactive elements"""
        # Arrange: HTML with no buttons/canvas
        empty_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Empty Game</title></head>
        <body>
            <h1>Test Game</h1>
            <p>This has no game elements</p>
        </body>
        </html>
        """

        # Act: Run verification
        verifier = GameVerificationService()
        result = await verifier.verify_game("test-project-id", empty_html)

        # Assert: Should fail
        assert result.passed == False, "Should fail for games with no interactive elements"
        assert any("interactive" in err.lower() or "button" in err.lower() or "canvas" in err.lower()
                   for err in result.errors), "Should mention missing interactive elements"


# This test will FAIL because GameVerificationService doesn't exist yet
# That's expected - RED phase of TDD
