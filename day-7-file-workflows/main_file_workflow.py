import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

# Initialize Anthropic client
anthropic_client = Anthropic(api_key=api_key)

CLAUDE_MODEL = "claude-haiku-4-5-20251001"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY_7_DIR = os.path.join(BASE_DIR, "day-7-file-workflows")
PRD_FILE_PATH = os.path.join(DAY_7_DIR, "sample_prd_complex.txt")


def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_text_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def analyze_prd(prd_text):
    prompt = f"""Analyze the following PRD and identify key components.

Focus on:
- product scope
- user types
- core features
- risks

PRD:
{prd_text}
"""

    response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=400,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def generate_executive_summary(prd_text):
    prompt = f"""Create a concise executive summary of this PRD.

PRD:
{prd_text}
"""

    response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=250,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def generate_implementation_plan(prd_text):
    prompt = f"""Create a practical implementation plan.

Include:
- phases
- key components
- dependencies

PRD:
{prd_text}
"""

    response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=600,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def validate_prd(prd_text):
    prompt = f"""Review the following PRD as an enterprise-grade product specification.

Return exactly these sections:

CLOSED GAPS
- List gaps that now appear sufficiently addressed
- If none, say: None

REMAINING CRITICAL GAPS
- List only unresolved gaps that materially weaken the solution
- Maximum 3
- Do NOT include stylistic improvements
- Do NOT include optional future enhancements
- If none, say: None

OPTIONAL FUTURE IMPROVEMENTS
- List only non-blocking improvements
- Maximum 5
- If none, say: None

PRD UPDATES
- Write only the exact content that should be added or clarified
- Format it so a human can review and approve it
- If none remain, say: None

Rules:
- Do NOT re-flag issues that are already reasonably addressed
- Do NOT escalate into endless edge-case analysis
- Focus on meaningful product, operational, and system completeness
- Treat a strong, buildable, enterprise-quality PRD as done enough

PRD:
{prd_text}
"""

    response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=900,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def extract_updates(validation_output):
    marker = "PRD UPDATES"
    if marker not in validation_output:
        return ""

    updates = validation_output.split(marker, 1)[1].strip()

    # Remove leading colon if model returns "PRD UPDATES:"
    if updates.startswith(":"):
        updates = updates[1:].strip()

    return updates


def has_no_remaining_critical_gaps(validation_output):
    lowered = validation_output.lower()
    if "remaining critical gaps" not in lowered:
        return False

    tail = lowered.split("remaining critical gaps", 1)[1][:160]
    return "none" in tail


def has_no_updates(validation_output):
    lowered = validation_output.lower()
    if "prd updates" not in lowered:
        return False

    tail = lowered.split("prd updates", 1)[1][:120]
    return "none" in tail


def apply_approved_updates(original_prd, approved_updates):
    approved_updates = approved_updates.strip()

    if not approved_updates:
        return original_prd

    return f"""{original_prd}

## Approved Updates

{approved_updates}
"""


def ask_user_to_approve_updates(updates_only):
    print("\n--- Proposed PRD Updates ---")
    print(updates_only)

    while True:
        user_choice = input(
            "\nApply these updates to the PRD? Type 'yes', 'no', or 'edit': "
        ).strip().lower()

        if user_choice == "yes":
            return updates_only

        if user_choice == "no":
            return ""

        if user_choice == "edit":
            print("\nPaste your edited update block below.")
            print("When finished, type a single line with: END")
            edited_lines = []

            while True:
                line = input()
                if line.strip() == "END":
                    break
                edited_lines.append(line)

            edited_updates = "\n".join(edited_lines).strip()
            return edited_updates

        print("Invalid input. Please type 'yes', 'no', or 'edit'.")


def run_file_workflow():
    prd_text = read_text_file(PRD_FILE_PATH)

    print("\n--- Raw PRD ---")
    print(prd_text)

    analysis_output = analyze_prd(prd_text)
    print("\n--- Analysis ---")
    print(analysis_output)

    summary_output = generate_executive_summary(prd_text)
    print("\n--- Executive Summary ---")
    print(summary_output)

    implementation_output = generate_implementation_plan(prd_text)
    print("\n--- Implementation Plan ---")
    print(implementation_output)

    validation_output = validate_prd(prd_text)
    print("\n--- Validation Output ---")
    print(validation_output)

    if has_no_remaining_critical_gaps(validation_output):
        print("\nNo remaining critical gaps. No changes needed.")
        final_prd = prd_text
    else:
        updates_only = extract_updates(validation_output)

        if not updates_only or has_no_updates(validation_output):
            print("\nNo usable updates were proposed.")
            final_prd = prd_text
        else:
            approved_updates = ask_user_to_approve_updates(updates_only)

            if approved_updates:
                final_prd = apply_approved_updates(prd_text, approved_updates)
                write_text_file(PRD_FILE_PATH, final_prd)
                print("\nApproved updates were written back to the main PRD file.")
            else:
                final_prd = prd_text
                print("\nNo updates were applied.")

    return f"""ANALYSIS:
{analysis_output}

EXECUTIVE SUMMARY:
{summary_output}

IMPLEMENTATION PLAN:
{implementation_output}

MAIN PRD FILE UPDATED:
{PRD_FILE_PATH}
"""


if __name__ == "__main__":
    print("Day 7 file workflow system initialized.")

    final_result = run_file_workflow()

    print("\n--- Final Output ---")
    print(final_result)