import subprocess


def run_git_command(args: list[str]) -> tuple[int, str, str]:
   result = subprocess.run(
       ["git"] + args,
       capture_output=True,
       text=True
   )
   return result.returncode, result.stdout, result.stderr


def create_and_checkout_branch(branch_name: str) -> dict:
   code, out, err = run_git_command(["checkout", "-b", branch_name])
   return {
       "success": code == 0,
       "stdout": out,
       "stderr": err
   }


def add_all_changes() -> dict:
   code, out, err = run_git_command(["add", "."])
   return {
       "success": code == 0,
       "stdout": out,
       "stderr": err
   }


def commit_changes(message: str) -> dict:
   code, out, err = run_git_command(["commit", "-m", message])
   return {
       "success": code == 0,
       "stdout": out,
       "stderr": err
   }


def push_branch(branch_name: str) -> dict:
   code, out, err = run_git_command(["push", "-u", "origin", branch_name])
   return {
       "success": code == 0,
       "stdout": out,
       "stderr": err
   }
