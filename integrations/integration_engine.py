import json
import os
from datetime import datetime

from payload_builder import build_task_payload, build_github_issue_payload
from api_client import post_json, post_github_issue
from response_validator import validate_integration_response


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TASK_PATH = os.path.join(
    BASE_DIR,
    "day-10-task-system",
    "tasks",
    "versions",
    "tasks_20260413_140855.json"
)

TARGET_URL = "https://httpbin.org/post"
GITHUB_URL = "https://api.github.com/repos/timmynyce/ai-integration-test/issues"


def load_tasks(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_results(results):
    os.makedirs(os.path.join(BASE_DIR, "integrations", "versions"), exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(BASE_DIR, "integrations", "versions", f"integrations_{ts}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return path


def run_httpbin_pipeline():
    tasks = load_tasks(TASK_PATH)
    results = []

    for t in tasks:
        payload = build_task_payload(t)
        status, body = post_json(TARGET_URL, payload)
        validation = validate_integration_response(status, body)

        results.append({
            "feature": t["feature"],
            "story": t["story"],
            "actor": t["actor"],
            "task_type": t["task_type"],
            "task": t["task"],
            "integration_target": TARGET_URL,
            "payload": payload,
            "response_status": status,
            "response_body": body,
            "response_valid": validation["valid"],
            "response_issues": validation["issues"]
        })

    print("httpbin pipeline complete")
    return results


def run_github_pipeline():
    tasks = load_tasks(TASK_PATH)
    results = []

    for t in tasks:
        payload = build_github_issue_payload(t)
        status, body = post_github_issue(GITHUB_URL, payload)
        validation = validate_integration_response(status, body)

        results.append({
            "feature": t["feature"],
            "story": t["story"],
            "actor": t["actor"],
            "task_type": t["task_type"],
            "task": t["task"],
            "integration_target": GITHUB_URL,
            "payload": payload,
            "response_status": status,
            "response_body": body,
            "response_valid": validation["valid"],
            "response_issues": validation["issues"]
        })

    print("GitHub pipeline complete")
    return results


if __name__ == "__main__":
    print("1 = httpbin")
    print("2 = GitHub")

    choice = input("Choose: ").strip()

    if choice == "2":
        results = run_github_pipeline()
    else:
        results = run_httpbin_pipeline()

    save_path = save_results(results)
    print("Saved integration results to:", save_path)

    print("\n--- SAMPLE RESULTS ---")
    for r in results[:3]:
        print({
            "task": r["task"],
            "response_status": r["response_status"],
            "response_valid": r["response_valid"],
            "response_issues": r["response_issues"]
        })