#!/usr/bin/env python3
"""
Example script to test the MCP server
"""

import json
import subprocess
import sys
from pathlib import Path

def run_example_request(request_data):
    """Run a single example request"""
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, '-m', 'src.main'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent.parent
        )

        # Send request
        request_json = json.dumps(request_data) + '\n'
        stdout, stderr = process.communicate(input=request_json, timeout=30)

        if stderr:
            print(f"Error: {stderr}")
            return None

        # Parse response
        response = json.loads(stdout.strip())
        return response

    except subprocess.TimeoutExpired:
        process.kill()
        print("Request timed out")
        return None
    except Exception as e:
        print(f"Error running request: {e}")
        return None

def main():
    """Run example requests"""

    # Load sample requests
    with open('examples/sample_requests.json', 'r') as f:
        examples = json.load(f)

    print("🚀 Running MCP Server Examples\n")

    for name, request in examples.items():
        print(f"📋 Running: {name}")
        print(f"Request: {json.dumps(request, indent=2)}")

        response = run_example_request(request)

        if response:
            print(f"Response: {json.dumps(response, indent=2)}")
        else:
            print("❌ Failed to get response")

        print("-" * 80)

if __name__ == "__main__":
    main()
