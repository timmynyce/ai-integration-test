import json
import os
import sys
from datetime import datetime

# -------------------------------------------------------------------
# PATH SETUP - makes the current mixed course folder structure work
# -------------------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

# Add current Day 15 folder so html_builder.py and git_helper.py can be imported
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

# Add day-folder engine locations directly to sys.path
DAY9_STORIES_DIR = os.path.join(BASE_DIR, "day-9-story-system", "stories")
DAY10_TASKS_DIR = os.path.join(BASE_DIR, "day-10-task-system", "tasks")

for path in [
    BASE_DIR,
    DAY9_STORIES_DIR,
    DAY10_TASKS_DIR,
    os.path.join(BASE_DIR, "prd"),
    os.path.join(BASE_DIR, "codegen"),
    os.path.join(BASE_DIR, "tests"),
    os.path.join(BASE_DIR, "integrations"),
    os.path.join(BASE_DIR, "governance"),
]:
    if path not in sys.path:
        sys.path.append(path)

# -------------------------------------------------------------------
# IMPORTS
# These imports now work with your existing folder setup
# -------------------------------------------------------------------

from html_builder import build_capstone_html
from git_helper import (
    create_and_checkout_branch,
    add_all_changes,
    commit_changes,
    push_branch,
)

from prd_engine import build_structured_prd_with_cto_gate
from story_engine import build_stories
from task_engine import build_tasks
from code_engine import build_code_pipeline
from test_engine import build_test_pipeline
from integration_engine import run_httpbin_pipeline, run_github_pipeline
from governance_engine import run_governance_pipeline

# -------------------------------------------------------------------
# OUTPUT PATHS
# -------------------------------------------------------------------

CAPSTONE_OUTPUT_PATH = os.path.join(CURRENT_DIR, "capstone_output.html")
CAPSTONE_SUMMARY_PATH = os.path.join(CURRENT_DIR, "capstone_summary.json")


def save_capstone_summary(summary: dict) -> str:
    with open(CAPSTONE_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return CAPSTONE_SUMMARY_PATH


def save_capstone_html(summary: dict) -> str:
    html = build_capstone_html(summary)
    with open(CAPSTONE_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    return CAPSTONE_OUTPUT_PATH


def summarize_results(stories, tasks, code_objects, tests, integration_results, governance_results) -> dict:
    sample_story_titles = []
    for story in stories[:5]:
        sample_story_titles.append(story.get("feature", ""))

    sample_tasks = []
    for task in tasks[:5]:
        sample_tasks.append(task.get("task", ""))

    sample_integration_targets = []
    for result in integration_results[:5]:
        sample_integration_targets.append(result.get("integration_target", ""))

    sample_governance_issues = []
    for result in governance_results[:5]:
        issues = result.get("output_issues", []) + result.get("input_issues", [])
        if issues:
            sample_governance_issues.extend(issues[:2])

    allowed_count = sum(1 for r in governance_results if r.get("allowed_to_proceed"))
    blocked_count = len(governance_results) - allowed_count

    return {
        "timestamp": datetime.now().isoformat(),
        "stories_count": len(stories),
        "tasks_count": len(tasks),
        "code_count": len(code_objects),
        "tests_count": len(tests),
        "integration_count": len(integration_results),
        "governance_count": len(governance_results),
        "governance_allowed_count": allowed_count,
        "governance_blocked_count": blocked_count,
        "sample_story_titles": sample_story_titles,
        "sample_tasks": sample_tasks,
        "sample_integration_targets": sample_integration_targets,
        "sample_governance_issues": sample_governance_issues
    }


def run_capstone_pipeline(use_github: bool = False) -> dict:
    print("\n--- STEP 1: PRD ---")
    prd = build_structured_prd_with_cto_gate()

    print("\n--- STEP 2: STORIES ---")
    stories = build_stories()

    print("\n--- STEP 3: TASKS ---")
    tasks = build_tasks()

    print("\n--- STEP 4: CODE ---")
    code_objects = build_code_pipeline()

    print("\n--- STEP 5: TESTS ---")
    tests = build_test_pipeline()

    print("\n--- STEP 6: INTEGRATION ---")
    if use_github:
        integration_results = run_github_pipeline()
    else:
        integration_results = run_httpbin_pipeline()

    print("\n--- STEP 7: GOVERNANCE ---")
    governance_results = run_governance_pipeline()

    print("\n--- STEP 8: FINAL SUMMARY ---")
    summary = summarize_results(
        stories=stories,
        tasks=tasks,
        code_objects=code_objects,
        tests=tests,
        integration_results=integration_results,
        governance_results=governance_results
    )

    summary_path = save_capstone_summary(summary)
    html_path = save_capstone_html(summary)

    print("Saved capstone summary to:", summary_path)
    print("Saved capstone HTML to:", html_path)

    return {
        "prd": prd,
        "stories": stories,
        "tasks": tasks,
        "code": code_objects,
        "tests": tests,
        "integration": integration_results,
        "governance": governance_results,
        "summary": summary,
        "summary_path": summary_path,
        "html_path": html_path
    }


def run_git_delivery(branch_name: str, commit_message: str, push_to_remote: bool) -> dict:
    print("\n--- STEP 10: GIT BRANCH ---")
    branch_result = create_and_checkout_branch(branch_name)
    print("Branch created:", branch_result["success"])

    print("\n--- STEP 11: GIT ADD ---")
    add_result = add_all_changes()
    print("Files staged:", add_result["success"])

    print("\n--- STEP 12: GIT COMMIT ---")
    commit_result = commit_changes(commit_message)
    print("Commit created:", commit_result["success"])

    push_result = {
        "success": False,
        "stdout": "",
        "stderr": "Push skipped"
    }

    if push_to_remote:
        print("\n--- STEP 13: GIT PUSH ---")
        push_result = push_branch(branch_name)
        print("Push success:", push_result["success"])

    return {
        "branch": branch_result,
        "add": add_result,
        "commit": commit_result,
        "push": push_result
    }


if __name__ == "__main__":
    print("Choose integration mode:")
    print("1 = httpbin")
    print("2 = GitHub")
    integration_choice = input("Choose (1 or 2): ").strip()

    use_github = integration_choice == "2"

    results = run_capstone_pipeline(use_github=use_github)

    print("\n--- STEP 9: LAUNCHABLE OUTPUT ---")
    print("Open this file in browser:")
    print(results["html_path"])
    print("Or serve locally with:")
    print("python -m http.server 8000")
    print("Then visit:")
    print("http://localhost:8000/day-15-capstone/capstone_output.html")

    print("\nChoose Git delivery mode:")
    print("1 = branch + commit only")
    print("2 = branch + commit + push")
    git_choice = input("Choose (1 or 2): ").strip()

    branch_name = input("Enter new branch name: ").strip()
    if not branch_name:
        branch_name = "capstone-final-output"

    commit_message = input("Enter commit message: ").strip()
    if not commit_message:
        commit_message = "Add final AI Product Builder capstone outputs"

    git_results = run_git_delivery(
        branch_name=branch_name,
        commit_message=commit_message,
        push_to_remote=(git_choice == "2")
    )

    print("\n--- FINAL SUMMARY ---")
    print("Stories count:", len(results["stories"]))
    print("Tasks count:", len(results["tasks"]))
    print("Code objects:", len(results["code"]))
    print("Tests generated:", len(results["tests"]))
    print("Integration results:", len(results["integration"]))
    print("Governed results:", len(results["governance"]))
    print("HTML output created:", os.path.exists(results["html_path"]))
    print("Git branch success:", git_results["branch"]["success"])
    print("Git commit success:", git_results["commit"]["success"])
    print("Git push success:", git_results["push"]["success"])