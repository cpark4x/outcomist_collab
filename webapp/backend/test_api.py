"""Test script for API endpoints (without requiring API key)."""

import asyncio
import sys

from src.database import ProjectType
from src.database import get_db
from src.database import init_db
from src.services import MessageService
from src.services import ProjectService
from src.services import SessionService


async def test_database_operations():
    """Test basic database operations."""
    print("\n=== Testing Database Operations ===\n")

    # Initialize database
    print("1. Initializing database...")
    await init_db()
    print("   ✓ Database initialized")

    # Get database session
    async for db in get_db():
        try:
            # Test 1: Create a project
            print("\n2. Creating a project...")
            project = await ProjectService.create_project(
                db,
                name="Test Game Project",
                description="A test adventure game",
                project_type=ProjectType.GAME,
            )
            print(f"   ✓ Created project: {project.id}")
            print(f"     Name: {project.name}")
            print(f"     Type: {project.type.value}")
            print(f"     Status: {project.status.value}")

            # Test 2: Get all projects
            print("\n3. Getting all projects...")
            projects = await ProjectService.get_all_projects(db)
            print(f"   ✓ Found {len(projects)} project(s)")

            # Test 3: Get specific project
            print("\n4. Getting specific project...")
            retrieved_project = await ProjectService.get_project(db, project.id)
            print(f"   ✓ Retrieved project: {retrieved_project.name}")

            # Test 4: Create a session
            print("\n5. Creating a session...")
            session = await SessionService.create_session(
                db,
                project_id=project.id,
                name="Main Design Session",
            )
            print(f"   ✓ Created session: {session.id}")
            print(f"     Name: {session.name}")
            print(f"     Status: {session.status.value}")

            # Test 5: Get project sessions
            print("\n6. Getting project sessions...")
            sessions = await SessionService.get_project_sessions(db, project.id)
            print(f"   ✓ Found {len(sessions)} session(s)")

            # Test 6: Create messages (without AI response)
            print("\n7. Creating test messages...")
            from src.database import MessageRole

            user_message = await MessageService.create_message(
                db,
                session_id=session.id,
                role=MessageRole.USER,
                content="Help me design a fantasy RPG",
            )
            print(f"   ✓ Created user message: {user_message.id}")

            ai_message = await MessageService.create_message(
                db,
                session_id=session.id,
                role=MessageRole.ASSISTANT,
                content="I'd be happy to help! Let's start by discussing...",
            )
            print(f"   ✓ Created AI message: {ai_message.id}")

            # Test 7: Get conversation history
            print("\n8. Getting conversation history...")
            messages = await MessageService.get_session_messages(db, session.id)
            print(f"   ✓ Found {len(messages)} message(s)")
            for msg in messages:
                print(f"     [{msg.role.value}]: {msg.content[:50]}...")

            # Test 8: Update project
            print("\n9. Updating project...")
            from src.database import ProjectStatus

            updated_project = await ProjectService.update_project(
                db,
                project_id=project.id,
                description="Updated description",
                status=ProjectStatus.ACTIVE,
            )
            print(f"   ✓ Updated project: {updated_project.description}")

            # Test 9: Delete project (cascade deletes sessions and messages)
            print("\n10. Deleting project...")
            deleted = await ProjectService.delete_project(db, project.id)
            print(f"   ✓ Project deleted: {deleted}")

            print("\n=== All Tests Passed! ===\n")

        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback

            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_database_operations())
