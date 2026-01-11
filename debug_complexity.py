
def analyze_complexity(messages: list) -> bool:
    combined_text = " ".join([m.get("content", "") for m in messages])
    print(f"DEBUG: Combined text: '{combined_text}'")
    # Expanded keywords for "Smart" routing based on user feedback
    complex_keywords = [
        "code", "function", "python", "javascript", "react", "sql", # Coding
        "story", "poem", "essay", "novel", "haiku", # Creative Writing
        "logic", "reasoning", "solve", "math", "calculus", # Critical Thinking
        "analysis", "summary", "extract" # Data Processing
    ]

    if any(keyword in combined_text.lower() for keyword in complex_keywords):
        print("DEBUG: Keyword found")
        return True
    if len(combined_text) > 800:
        print("DEBUG: Length > 800")
        return True
    return False

test_messages = [{"role": "user", "content": "Write a short story about a cat, but do not use the letter 'e' in any word."}]
is_complex = analyze_complexity(test_messages)
print(f"Is Complex? {is_complex}")
