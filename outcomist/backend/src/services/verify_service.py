"""Minimal game verification using Playwright - TDD implementation"""

from dataclasses import dataclass
from pathlib import Path
import tempfile
import logging
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

from ..database.models import File as FileModel

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    """Results from game verification"""
    passed: bool
    errors: list[str]
    console_logs: list[str]
    screenshot_path: str | None = None


class GameVerificationService:
    """Verify games work using Playwright headless browser"""

    async def verify_project_game(self, db: AsyncSession, project_id: str) -> VerificationResult:
        """
        Verify a game project by bundling files and running verification.

        Args:
            db: Database session
            project_id: UUID of the project

        Returns:
            VerificationResult with pass/fail
        """
        # Get all files for the project
        result = await db.execute(
            select(FileModel).where(FileModel.project_id == project_id)
        )
        files = list(result.scalars().all())

        if not files:
            return VerificationResult(
                passed=False,
                errors=["No files found in project"],
                console_logs=[],
                screenshot_path=None
            )

        # Bundle files into single HTML
        bundled_html = await self._bundle_game_files(files)

        if not bundled_html:
            return VerificationResult(
                passed=False,
                errors=["No HTML file found to verify"],
                console_logs=[],
                screenshot_path=None
            )

        # Run verification on bundled HTML
        return await self.verify_game(project_id, bundled_html)

    async def _bundle_game_files(self, files: list[FileModel]) -> str | None:
        """Bundle HTML, CSS, and JS files into single HTML file."""
        # Find HTML file
        html_file = None
        for f in files:
            if f.name.endswith('.html'):
                html_file = f
                break

        if not html_file:
            return None

        # Read HTML content
        html_path = Path(html_file.path)
        html_content = html_path.read_text()

        # Inline CSS files
        css_files = [f for f in files if f.name.endswith('.css')]
        for css_file in css_files:
            css_path = Path(css_file.path)
            css_content = css_path.read_text()

            # Replace <link> tag with inline <style>
            link_pattern = f'<link[^>]*href=["\']{ re.escape(css_file.name)}["\'][^>]*>'
            html_content = re.sub(
                link_pattern,
                f'<style>{css_content}</style>',
                html_content,
                flags=re.IGNORECASE
            )

        # Inline JS files
        js_files = [f for f in files if f.name.endswith('.js')]
        for js_file in js_files:
            js_path = Path(js_file.path)
            js_content = js_path.read_text()

            # Replace <script src> with inline <script>
            script_pattern = f'<script[^>]*src=["\']{ re.escape(js_file.name)}["\'][^>]*></script>'
            html_content = re.sub(
                script_pattern,
                f'<script>{js_content}</script>',
                html_content,
                flags=re.IGNORECASE
            )

        return html_content

    async def verify_game(self, project_id: str, game_html: str) -> VerificationResult:
        """
        Verify game works by running in headless browser.

        Minimal tests:
        1. Page loads without crash
        2. No console errors
        3. Has interactive elements (button/canvas/input)

        Args:
            project_id: Project ID
            game_html: Complete HTML content

        Returns:
            VerificationResult with pass/fail
        """
        errors: list[str] = []
        console_logs: list[str] = []

        # Save HTML to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(game_html)
            temp_path = f.name

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Capture console messages
                def handle_console(msg):
                    log_entry = f"[{msg.type}] {msg.text}"
                    console_logs.append(log_entry)
                    if msg.type == "error":
                        errors.append(f"Console error: {msg.text}")

                page.on("console", handle_console)

                # Capture page errors
                def handle_page_error(error):
                    errors.append(f"Page error: {error}")

                page.on("pageerror", handle_page_error)

                # Test 1: Page loads
                try:
                    await page.goto(f"file://{temp_path}", wait_until="networkidle", timeout=10000)
                except Exception as e:
                    errors.append(f"Page load failed: {str(e)}")
                    await browser.close()
                    Path(temp_path).unlink(missing_ok=True)
                    return VerificationResult(False, errors, console_logs, None)

                # Wait for JS to execute
                await page.wait_for_timeout(2000)

                # Test 2: Check for interactive elements
                try:
                    buttons = await page.query_selector_all("button")
                    canvases = await page.query_selector_all("canvas")
                    inputs = await page.query_selector_all("input, select, textarea")

                    if len(buttons) == 0 and len(canvases) == 0 and len(inputs) == 0:
                        errors.append("No interactive elements found (no buttons, canvas, or inputs)")
                except Exception as e:
                    errors.append(f"Element check failed: {str(e)}")

                await browser.close()

        except Exception as e:
            errors.append(f"Verification failed: {str(e)}")
        finally:
            Path(temp_path).unlink(missing_ok=True)

        passed = len(errors) == 0
        return VerificationResult(passed, errors, console_logs, None)
