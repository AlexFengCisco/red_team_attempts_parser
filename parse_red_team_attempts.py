#!/usr/bin/env python3
"""
Red Team Attempts Parser
Parses red_team_attempts.jsonl file and displays content in a readable format.
"""

import json
import sys
from pathlib import Path


def parse_transcript(transcript):
    """
    Parse the transcript string and separate Human and Assistant messages.
    Returns a list of tuples: (speaker, message)
    """
    lines = []
    current_speaker = None
    current_message = []

    # Split transcript by the markers
    parts = transcript.split('\n\n')

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if part.startswith('Human:'):
            # Save previous message if exists
            if current_speaker and current_message:
                lines.append((current_speaker, ' '.join(current_message).strip()))
                current_message = []

            current_speaker = 'Human'
            message = part[6:].strip()  # Remove 'Human:' prefix
            current_message.append(message)

        elif part.startswith('Assistant:'):
            # Save previous message if exists
            if current_speaker and current_message:
                lines.append((current_speaker, ' '.join(current_message).strip()))
                current_message = []

            current_speaker = 'Assistant'
            message = part[10:].strip()  # Remove 'Assistant:' prefix
            current_message.append(message)
        else:
            # Continue current message
            if current_speaker:
                current_message.append(part)

    # Don't forget the last message
    if current_speaker and current_message:
        lines.append((current_speaker, ' '.join(current_message).strip()))

    return lines


def format_conversation(entry, index):
    """Format a single conversation entry for display."""
    output = []
    output.append("=" * 80)
    output.append(f"CONVERSATION #{index}")
    output.append("=" * 80)
    output.append(f"Task Description: {entry.get('task_description', 'N/A')}")
    output.append(f"Rating: {entry.get('rating', 'N/A')}")
    output.append(f"Model Type: {entry.get('model_type', 'N/A')}")
    output.append(f"Parameters: {entry.get('num_params', 'N/A')}")
    output.append(f"Min Harmlessness Score: {entry.get('min_harmlessness_score_transcript', 'N/A')}")
    output.append(f"Red Team Member ID: {entry.get('red_team_member_id', 'N/A')}")
    output.append(f"Is Upworker: {entry.get('is_upworker', 'N/A')}")
    output.append("-" * 80)
    output.append("TRANSCRIPT:")
    output.append("-" * 80)

    # Parse and format the conversation
    transcript = entry.get('transcript', '')
    conversation = parse_transcript(transcript)

    for speaker, message in conversation:
        if speaker == 'Human':
            output.append(f"\n👤 HUMAN:")
            output.append(f"   {message}")
        else:
            output.append(f"\n🤖 ASSISTANT:")
            output.append(f"   {message}")

    output.append("\n")
    return '\n'.join(output)


def main():
    # File path
    file_path = Path(__file__).parent / 'red_team_attempts.jsonl'

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Parse red team attempts JSONL file')
    parser.add_argument('-n', '--num', type=int, default=5,
                        help='Number of conversations to display (default: 5)')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Display all conversations')
    parser.add_argument('-o', '--output', type=str,
                        help='Save output to file instead of printing to console')
    parser.add_argument('--start', type=int, default=0,
                        help='Start from this conversation index (0-based)')
    args = parser.parse_args()

    print("Red Team Attempts Parser")
    print("=" * 80)
    print("Loading data... This may take a moment for large files.")

    # Read and parse the entire JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("Error: Expected JSON array in file")
            sys.exit(1)

        total_conversations = len(data)
        print(f"Total conversations in file: {total_conversations}")

        # Determine number to display
        if args.all:
            num_to_display = total_conversations
        else:
            num_to_display = min(args.num, total_conversations - args.start)

        if args.start >= total_conversations:
            print(f"Error: Start index {args.start} is beyond the total {total_conversations} conversations")
            sys.exit(1)

        # Determine output destination
        save_to_file = args.output is not None
        output_file = None

        if save_to_file:
            output_file = Path(__file__).parent / args.output

        # Process the conversations
        print(f"\nProcessing {num_to_display} conversation(s) starting from index {args.start}...\n")

        output_lines = []
        end_index = min(args.start + num_to_display, total_conversations)

        for i in range(args.start, end_index):
            entry = data[i]
            formatted = format_conversation(entry, i + 1)

            if save_to_file:
                output_lines.append(formatted)
            else:
                print(formatted)

        # Save to file if requested
        if save_to_file and output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            print(f"\n✓ Output saved to: {output_file}")

        print(f"\n✓ Processing complete! Displayed {num_to_display} conversation(s).")

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
