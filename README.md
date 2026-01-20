# Red Team Attempts Parser

This Python script parses the Anthropic `red_team_attempts.jsonl` file and displays conversations in an easy-to-read format with clear separation between human and assistant messages.

## Features

- ✅ Parses large JSONL files containing red team conversation attempts
- ✅ Separates Human and Assistant messages with clear visual indicators (👤 and 🤖)
- ✅ Displays metadata including task description, ratings, and harmlessness scores
- ✅ Supports outputting to console or saving to file
- ✅ Can display specific range of conversations
- ✅ Handles large files (38,961 conversations)

## Usage

### Basic Usage

Display first 5 conversations (default):
```bash
python parse_red_team_attempts.py
```

### Display Specific Number of Conversations

Display first 10 conversations:
```bash
python parse_red_team_attempts.py -n 10
```

### Save to File

Save first 20 conversations to a file:
```bash
python parse_red_team_attempts.py -n 20 -o output.txt
```

### Start from Specific Index

Display 10 conversations starting from index 100:
```bash
python parse_red_team_attempts.py -n 10 --start 100
```

### Display All Conversations

⚠️ Warning: This will display all 38,961 conversations (may take a while):
```bash
python parse_red_team_attempts.py -a -o all_conversations.txt
```

## Command-Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--num` | `-n` | Number of conversations to display | 5 |
| `--all` | `-a` | Display all conversations | False |
| `--output` | `-o` | Save to file instead of printing | None |
| `--start` | | Start from this conversation index (0-based) | 0 |

## Output Format

Each conversation includes:

```
================================================================================
CONVERSATION #1
================================================================================
Task Description: [Description of the red team task]
Rating: [0.0 - 4.0]
Model Type: [e.g., context distillation]
Parameters: [e.g., 52B]
Min Harmlessness Score: [Score]
Red Team Member ID: [ID]
Is Upworker: [True/False]
--------------------------------------------------------------------------------
TRANSCRIPT:
--------------------------------------------------------------------------------

👤 HUMAN:
   [Human's message]

🤖 ASSISTANT:
   [Assistant's response]

👤 HUMAN:
   [Next human message]

🤖 ASSISTANT:
   [Next assistant response]
```

## Examples

1. **Quick preview** - See first 3 conversations:
   ```bash
   python parse_red_team_attempts.py -n 3
   ```

2. **Export sample** - Save first 50 to review later:
   ```bash
   python parse_red_team_attempts.py -n 50 -o sample.txt
   ```

3. **Browse middle section** - See conversations 1000-1050:
   ```bash
   python parse_red_team_attempts.py --start 1000 -n 50
   ```

## File Information

- **Input file**: `red_team_attempts.jsonl`
- **Format**: JSON array containing 38,961 conversation objects
- **File size**: ~52.9 MB
- **Structure**: Each conversation contains transcript, ratings, metadata

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Notes

- The file contains red team testing conversations used to evaluate AI safety
- Conversations include various challenging scenarios and edge cases
- Some content may be offensive or controversial as it's designed to test model boundaries
