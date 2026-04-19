def build_happy_path_test(function_name: str, task_type: str) -> str:
    if task_type == "validation":
        return f"""def test_{function_name}_happy():
    result = {function_name}({{"sample": "value"}})
    assert isinstance(result, (bool, dict))
"""

    if task_type == "integration":
        return f"""def test_{function_name}_happy():
    result = {function_name}({{"amount": 5000, "currency": "usd"}})
    assert isinstance(result, dict)
    assert "status" in result or "payload" in result or "task" in result
"""

    if task_type == "data":
        return f"""def test_{function_name}_happy():
    result = {function_name}({{"id": 1, "name": "sample"}})
    assert isinstance(result, dict)
"""

    if task_type == "frontend":
        return f"""def test_{function_name}_happy():
    result = {function_name}({{"title": "Sample"}})
    assert isinstance(result, dict)
    assert "view_state" in result or "data" in result
"""

    return f"""def test_{function_name}_happy():
    result = {function_name}()
    assert isinstance(result, dict)
    assert "status" in result or "success" in result or "task" in result
"""


def build_failure_test(function_name: str, task_type: str) -> str:
    if task_type == "validation":
        return f"""def test_{function_name}_failure():
    result = {function_name}(None)
    assert result is False or isinstance(result, dict)
"""

    if task_type == "integration":
        return f"""def test_{function_name}_failure():
    result = {function_name}({{"amount": 0}})
    assert isinstance(result, dict)
"""

    if task_type == "data":
        return f"""def test_{function_name}_failure():
    try:
        result = {function_name}(None)
        assert result is not None
    except TypeError:
        assert True
"""

    if task_type == "frontend":
        return f"""def test_{function_name}_failure():
    result = {function_name}({{}})
    assert isinstance(result, dict)
"""

    return f"""def test_{function_name}_failure():
    try:
        result = {function_name}(None)
        assert isinstance(result, dict)
    except TypeError:
        assert True
"""


def generate_test_cases(code_objects):
    tests = []

    for obj in code_objects:
        task = obj["task"]
        task_type = obj["task_type"]
        code = obj["code"]

        if "def " not in code:
            continue

        function_name = code.split("def ")[1].split("(")[0]

        tests.append({
            "feature": obj["feature"],
            "task": task,
            "task_type": task_type,
            "test_type": "happy_path",
            "test_code": build_happy_path_test(function_name, task_type)
        })

        tests.append({
            "feature": obj["feature"],
            "task": task,
            "task_type": task_type,
            "test_type": "failure",
            "test_code": build_failure_test(function_name, task_type)
        })

    return tests