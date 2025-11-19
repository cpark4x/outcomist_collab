"""Integration test for game verification with database

Tests the full flow: Project -> Files -> Verification
"""

import pytest
import pytest_asyncio
import sys
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.models import Base, Project, File as FileModel, ProjectType
from src.services.verify_service import GameVerificationService


# Test database setup
@pytest_asyncio.fixture
async def db_session():
    """Create a test database session"""
    # Use in-memory SQLite for tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestGameVerificationIntegration:
    """Test game verification with actual database and files"""

    @pytest.mark.asyncio
    async def test_verifies_broken_game_with_files(self, db_session, temp_dir):
        """Test that verification catches broken games with actual file storage"""
        # Create a project
        project = Project(
            id="test-project-123",
            type=ProjectType.GAME,
            name="Broken Test Game"
        )
        db_session.add(project)
        await db_session.commit()

        # Create broken HTML file
        html_path = temp_dir / "game.html"
        html_path.write_text("""
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
        """)

        # Create file record in database
        file_record = FileModel(
            project_id="test-project-123",
            name="game.html",
            path=str(html_path),
            mime_type="text/html",
            size=html_path.stat().st_size
        )
        db_session.add(file_record)
        await db_session.commit()

        # Run verification
        verifier = GameVerificationService()
        result = await verifier.verify_project_game(db_session, "test-project-123")

        # Assert: Should fail
        assert result.passed == False, "Should fail for games with console errors"
        assert len(result.errors) > 0, "Should have error messages"
        assert any("undefinedFunction" in err or "not defined" in err.lower() for err in result.errors), \
            f"Should detect undefined function error. Got: {result.errors}"

    @pytest.mark.asyncio
    async def test_verifies_working_game_with_files(self, db_session, temp_dir):
        """Test that verification passes for working games with actual file storage"""
        # Create a project
        project = Project(
            id="test-project-456",
            type=ProjectType.GAME,
            name="Working Test Game"
        )
        db_session.add(project)
        await db_session.commit()

        # Create working HTML file
        html_path = temp_dir / "game.html"
        html_path.write_text("""
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
        """)

        # Create file record in database
        file_record = FileModel(
            project_id="test-project-456",
            name="game.html",
            path=str(html_path),
            mime_type="text/html",
            size=html_path.stat().st_size
        )
        db_session.add(file_record)
        await db_session.commit()

        # Run verification
        verifier = GameVerificationService()
        result = await verifier.verify_project_game(db_session, "test-project-456")

        # Assert: Should pass
        assert result.passed == True, f"Should pass for working games. Errors: {result.errors}"
        assert len(result.errors) == 0, f"Should have no errors. Got: {result.errors}"

    @pytest.mark.asyncio
    async def test_verifies_game_with_multiple_files(self, db_session, temp_dir):
        """Test that verification works with separate HTML, CSS, and JS files"""
        # Create a project
        project = Project(
            id="test-project-789",
            type=ProjectType.GAME,
            name="Multi-file Test Game"
        )
        db_session.add(project)
        await db_session.commit()

        # Create HTML file
        html_path = temp_dir / "index.html"
        html_path.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>Multi-file Game</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Test Game</h1>
    <button id="start">Start</button>
    <canvas id="game"></canvas>
    <script src="game.js"></script>
</body>
</html>
        """)

        # Create CSS file
        css_path = temp_dir / "style.css"
        css_path.write_text("""
body { background: #000; color: #fff; }
canvas { border: 1px solid #fff; }
        """)

        # Create JS file (with no errors)
        js_path = temp_dir / "game.js"
        js_path.write_text("""
document.getElementById('start').addEventListener('click', function() {
    console.log('Game started');
    const canvas = document.getElementById('game');
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#fff';
    ctx.fillRect(10, 10, 50, 50);
});
        """)

        # Create file records
        mime_types = {"html": "text/html", "css": "text/css", "js": "application/javascript"}
        for name, path in [("index.html", html_path), ("style.css", css_path), ("game.js", js_path)]:
            ext = name.split('.')[-1]
            file_record = FileModel(
                project_id="test-project-789",
                name=name,
                path=str(path),
                mime_type=mime_types.get(ext, "text/plain"),
                size=path.stat().st_size
            )
            db_session.add(file_record)

        await db_session.commit()

        # Run verification
        verifier = GameVerificationService()
        result = await verifier.verify_project_game(db_session, "test-project-789")

        # Assert: Should pass
        assert result.passed == True, f"Should pass for working multi-file games. Errors: {result.errors}"
        assert len(result.errors) == 0, f"Should have no errors. Got: {result.errors}"

    @pytest.mark.asyncio
    async def test_handles_missing_files_gracefully(self, db_session, temp_dir):
        """Test that verification handles missing files without crashing"""
        # Create a project
        project = Project(
            id="test-project-missing",
            type=ProjectType.GAME,
            name="Missing Files Game"
        )
        db_session.add(project)
        await db_session.commit()

        # Create file record pointing to non-existent file
        file_record = FileModel(
            project_id="test-project-missing",
            name="game.html",
            path="/nonexistent/path/game.html",
            mime_type="text/html",
            size=0
        )
        db_session.add(file_record)
        await db_session.commit()

        # Run verification
        verifier = GameVerificationService()
        result = await verifier.verify_project_game(db_session, "test-project-missing")

        # Assert: Should fail gracefully
        assert result.passed == False, "Should fail for games with missing files"
        assert len(result.errors) > 0, "Should report error about missing file"
