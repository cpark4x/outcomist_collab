#!/usr/bin/env python3
"""
E2E Test for Game Verification
Tests that verification actually runs when games are generated
"""

import asyncio
import httpx
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

async def create_project_and_test(project_name: str, game_prompt: str, should_pass: bool):
    """Create a project and test verification"""
    print(f"\n{'='*80}")
    print(f"Test: {project_name}")
    print(f"Prompt: {game_prompt}")
    print(f"Expected: {'PASS' if should_pass else 'FAIL'} verification")
    print(f"{'='*80}\n")

    async with httpx.AsyncClient(timeout=300.0) as client:
        # Create project
        print("📝 Creating project...")
        response = await client.post(
            f"{BASE_URL}/api/projects",
            json={
                "name": project_name,
                "type": "game",
                "description": game_prompt
            }
        )
        project_data = response.json()
        project_id = project_data["id"]
        print(f"✅ Project created: {project_id}")

        # Create session
        print("🔌 Creating session...")
        response = await client.post(
            f"{BASE_URL}/api/sessions",
            json={"project_id": project_id}
        )
        session_data = response.json()
        session_id = session_data["id"]
        print(f"✅ Session created: {session_id}")

        # Send message (this triggers AI generation)
        print("💬 Sending message to AI...")
        print(f"   Message: {game_prompt}")

        response = await client.post(
            f"{BASE_URL}/api/messages",
            json={
                "session_id": session_id,
                "content": game_prompt,
                "role": "user"
            }
        )
        print(f"✅ Message sent")

        # Stream the response
        print("\n🎬 Streaming AI response...")
        print("-" * 80)

        verification_ran = False
        verification_passed = None
        verification_errors = []

        async with client.stream(
            "GET",
            f"{BASE_URL}/api/ai/stream/{session_id}"
        ) as stream_response:
            async for line in stream_response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix
                    if data_str == "[DONE]":
                        print("\n✅ Stream complete")
                        break

                    try:
                        event_data = json.loads(data_str)
                        event_type = event_data.get("type")

                        if event_type == "message_delta":
                            # Print content chunks
                            content = event_data.get("content", "")
                            if content:
                                print(content, end="", flush=True)

                                # Check for verification messages in content
                                if "Verification" in content or "verification" in content:
                                    verification_ran = True
                                if "PASSED" in content or "passed" in content:
                                    verification_passed = True
                                if "FAILED" in content or "failed" in content:
                                    verification_passed = False
                                if "⚠️" in content or "issues:" in content:
                                    verification_errors.append(content)

                        elif event_type == "status":
                            status = event_data.get("status")
                            print(f"\n[STATUS: {status}]")

                    except json.JSONDecodeError:
                        pass

        print("\n" + "-" * 80)

        # Check project final status
        print("\n📊 Checking final project status...")
        response = await client.get(f"{BASE_URL}/api/projects/{project_id}")
        final_project = response.json()
        final_status = final_project.get("status")
        print(f"   Final status: {final_status}")

        # Print verification summary
        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY:")
        print(f"  Verification ran: {verification_ran}")
        print(f"  Verification passed: {verification_passed}")
        if verification_errors:
            print(f"  Errors detected: {len(verification_errors)}")
            for err in verification_errors[:3]:  # Show first 3
                print(f"    - {err.strip()}")
        print(f"  Final project status: {final_status}")

        # Determine test result
        if should_pass:
            test_passed = verification_passed == True and final_status == "complete"
            expected_msg = "Verification should PASS"
        else:
            test_passed = verification_passed == False
            expected_msg = "Verification should FAIL"

        print(f"\n  Expected: {expected_msg}")
        print(f"  Result: {'✅ TEST PASSED' if test_passed else '❌ TEST FAILED'}")
        print("=" * 80)

        return test_passed

async def main():
    """Run E2E tests"""
    print("\n" + "🧪" * 40)
    print("E2E VERIFICATION TESTS - Phase 1")
    print("🧪" * 40)

    results = []

    # Test 1: Broken Snake game (should FAIL verification)
    test1_passed = await create_project_and_test(
        project_name="Test: Broken Snake",
        game_prompt="Create a Snake game but add a line 'undefinedFunction();' in the JavaScript to break it",
        should_pass=False
    )
    results.append(("T2-S1: Broken Snake", test1_passed))

    # Wait between tests
    print("\n⏳ Waiting 5 seconds before next test...\n")
    await asyncio.sleep(5)

    # Test 2: Working Snake game (should PASS verification)
    test2_passed = await create_project_and_test(
        project_name="Test: Working Snake",
        game_prompt="Create a simple Snake game with canvas, keyboard controls, and score display",
        should_pass=True
    )
    results.append(("T2-S2: Working Snake", test2_passed))

    # Final summary
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS:")
    print("=" * 80)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")

    all_passed = all(passed for _, passed in results)
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️ SOME TESTS FAILED")
    print("=" * 80)

    return all_passed

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        exit(2)
    except Exception as e:
        print(f"\n\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
