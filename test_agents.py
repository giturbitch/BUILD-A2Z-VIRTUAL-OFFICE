#!/usr/bin/env python3
"""
Quick test script to verify agents are working.
Run this after starting the server with: python run.py
"""

import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_health():
    """Test if server is running."""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{API_URL}/health")
        data = response.json()
        print(f"✓ Server is running")
        print(f"  Status: {data['status']}")
        print(f"  Scheduler: {'Running' if data['scheduler_running'] else 'Stopped'}")
        return True
    except Exception as e:
        print(f"✗ Server is not responding: {e}")
        print(f"  Make sure you ran: python run.py")
        return False

def test_agent_status():
    """Get status of all agents."""
    print_section("2. Agent Status")
    try:
        response = requests.get(f"{API_URL}/agents/status")
        data = response.json()
        for agent_name, status in data.items():
            print(f"\n  {agent_name.upper()}")
            print(f"    Last run: {status.get('last_run') or 'Never'}")
            print(f"    Next run: {status.get('next_run') or 'TBD'}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_run_agent(agent_name):
    """Run an agent and see results."""
    print_section(f"3. Running {agent_name.upper()} Agent")
    try:
        print(f"Triggering {agent_name} agent...")
        response = requests.post(f"{API_URL}/agents/{agent_name}/run")

        if response.status_code != 200:
            print(f"✗ Agent failed: {response.text}")
            return False

        result = response.json()
        print(f"✓ Agent executed successfully")
        print(f"\nResults:")
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_view_tasks():
    """View recent tasks."""
    print_section("4. Recent Tasks")
    try:
        response = requests.get(f"{API_URL}/tasks?limit=5")
        tasks = response.json()

        if not tasks:
            print("  No tasks yet. Run an agent first!")
            return True

        print(f"  Found {len(tasks)} recent tasks:\n")
        for task in tasks:
            print(f"  Task ID: {task['id']}")
            print(f"    Agent: {task['agent_name']}")
            print(f"    Status: {task['status']}")
            print(f"    Created: {task['created_at']}")
            print()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_view_content():
    """View generated content."""
    print_section("5. Generated Content")
    try:
        response = requests.get(f"{API_URL}/content?limit=10")
        content = response.json()

        if not content:
            print("  No content generated yet. Run the social media agent!")
            return True

        print(f"  Found {len(content)} content pieces:\n")
        for item in content[:5]:  # Show first 5
            print(f"  Platform: {item['platform'].upper()}")
            print(f"    Status: {item['status']}")
            print(f"    Content: {item['content'][:80]}...")
            print(f"    Created: {item['created_at']}\n")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║       Virtual AI Office - Agent Test Suite                  ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Run all tests
    if not test_health():
        return

    test_agent_status()

    # Ask if they want to run an agent
    print("\n" + "="*60)
    response = input("\n▶ Run Social Media Agent now? (y/n): ").lower()
    if response == 'y':
        test_run_agent("social_media")
        time.sleep(2)
        test_view_tasks()
        test_view_content()

    print("\n" + "="*60)
    print("\n✓ All tests completed!")
    print("\nNext steps:")
    print("  1. Open dashboard: http://localhost:8000/dashboard")
    print("  2. Click 'Run Social Media Agent Now' to generate content")
    print("  3. View generated content in the Recent Tasks section")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
