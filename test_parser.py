# test_parser.py
import warnings
warnings.filterwarnings("ignore")

from app.agent.parser import parse_steps

print("Testing Parser Fix...")
print("-" * 40)

# Test 1 - Normal multiline response (your exact case)
test1 = """[
  {"action": "open_url", "value": "https://www.google.com"},
  {"action": "screenshot", "value": "google_screenshot.png"}
]"""

print("\nTest 1 - Multiline JSON:")
result = parse_steps(test1)
print(f"Result: {result}")
print(f"Pass: {'✅' if len(result) == 2 else '❌'}")

# Test 2 - With markdown
test2 = """```json
[
  {"action": "open_url", "value": "https://google.com"},
  {"action": "click", "selector": "#search"}
]
```"""

print("\nTest 2 - With markdown:")
result = parse_steps(test2)
print(f"Result: {result}")
print(f"Pass: {'✅' if len(result) == 2 else '❌'}")

# Test 3 - Single line
test3 = '[{"action": "open_url", "value": "https://google.com"}]'

print("\nTest 3 - Single line:")
result = parse_steps(test3)
print(f"Result: {result}")
print(f"Pass: {'✅' if len(result) == 1 else '❌'}")

print("\n" + "-" * 40)
print("Parser test complete!")