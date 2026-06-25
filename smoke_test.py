#!/usr/bin/env python3
"""
Smoke tests against the running Docker container.
Run after `docker compose up` to verify key pages work.

Usage:
    python smoke_test.py
    python smoke_test.py --base-url http://localhost:8000
"""

import argparse
import subprocess
import sys

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

BASE_URL = "http://localhost:8000"


def get(path, expected_status=200):
    url = BASE_URL + path
    try:
        response = requests.get(url, allow_redirects=False, timeout=10)
        actual = response.status_code
    except Exception as e:
        return False, f"ERROR: {e}"

    ok = actual == expected_status
    return ok, f"HTTP {actual}"


def get_recipe_urls():
    """Fetch a sample of recipe URLs from the running container."""
    try:
        result = subprocess.run(
            [
                "docker", "compose", "exec", "-T", "web",
                "python", "manage.py", "shell", "-c",
                "from recipes.models import RecipePage; "
                "[print(p.url) for p in RecipePage.objects.live()[:5]]"
            ],
            capture_output=True, text=True, timeout=15,
            cwd=__file__.rsplit("/", 1)[0]
        )
        return [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    except Exception:
        return []


def run_tests():
    results = []

    def check(label, path, expected_status=200, note=""):
        ok, detail = get(path, expected_status)
        if note:
            detail += f" ({note})"
        status = "PASS" if ok else "FAIL"
        results.append((ok, f"  [{status}] {label} ({path}) — {detail}"))

    print(f"Running smoke tests against {BASE_URL}\n")

    # Django system checks
    try:
        result = subprocess.run(
            ["docker", "compose", "exec", "-T", "web", "python", "manage.py", "check"],
            capture_output=True, text=True, timeout=30,
            cwd=__file__.rsplit("/", 1)[0]
        )
        ok = result.returncode == 0
        results.append((ok, f"  [{'PASS' if ok else 'FAIL'}] Django system checks"))
    except Exception as e:
        results.append((False, f"  [FAIL] Django system checks — {e}"))

    # Core pages
    check("Homepage", "/")
    check("Search page", "/search/")
    check("Random recipe page", "/random/")
    check("Wagtail admin (redirects to login)", "/admin/", expected_status=302)

    # A category page
    check("Category listing", "/categories/beans-grains/beans/")

    # Sample recipe pages from the live DB
    recipe_urls = get_recipe_urls()
    if recipe_urls:
        for url in recipe_urls:
            check(f"Recipe: {url}", url)
    else:
        results.append((False, "  [FAIL] Could not fetch recipe URLs from container"))

    # Print results
    passed = sum(1 for ok, _ in results if ok)
    total = len(results)
    for _, line in results:
        print(line)
    print(f"\n{passed}/{total} passed")

    return all(ok for ok, _ in results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    args = parser.parse_args()
    BASE_URL = args.base_url.rstrip("/")

    success = run_tests()
    sys.exit(0 if success else 1)
