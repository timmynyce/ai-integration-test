- Agent selected a reasonable comparison path
- Final output was cut off mid-response
- Likely needs stronger compare prompt and/or higher max_tokens
- Agent may be finalizing too early

- Adding this to the compare_text function helped greatly improve the output 
```
Return these sections:
- Concept 1
- Concept 2
- Key Differences
- When to Use Each
- Simple Example

Be complete, specific, and beginner-friendly.
```