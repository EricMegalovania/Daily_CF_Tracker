import re
import os
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_from_directory
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BASE_DIR = Path(os.getenv("REPO_PATH", Path(__file__).resolve().parent.parent))
DAILY_DIR = BASE_DIR / "daily_problems"


def problem_code_to_filename(code: str) -> str:
    m = re.match(r"^(?:GYM|CF)(\d+)(\w+)$", code, re.IGNORECASE)
    if not m:
        return code.lower()
    return ("cf" + m.group(1) + m.group(2)).lower()


def parse_problems_md(filepath: Path) -> list[dict]:
    results = []
    if not filepath.exists():
        return results
    text = filepath.read_text(encoding="utf-8")
    for m in re.finditer(
        r"\|\s*(\*?\d+)\s*\|\s*\[(\w+)\]\(([^)]+)\)\s*\|\s*(.+?)\s*\|",
        text,
    ):
        diff = m.group(1)
        code = m.group(2)
        url = m.group(3)
        hint = m.group(4)
        file_code = problem_code_to_filename(code)
        results.append(
            {
                "difficulty": diff,
                "code": code,
                "file_code": file_code,
                "url": url,
                "hint": hint,
            }
        )
    return results


def check_submission(day_dir: Path, file_code: str, username: str) -> bool:
    sub_dir = day_dir / "personal_submission"
    if not sub_dir.is_dir():
        return False
    prefix = file_code.lower() + "_"
    user_lower = username.lower()
    for f in sub_dir.iterdir():
        if f.name == ".gitkeep":
            continue
        name = f.stem.lower()
        if name.startswith(prefix) and ("_" + user_lower) in name:
            return True
    return False


def get_date_dirs(reverse: bool = True) -> list[Path]:
    dirs = []
    if not DAILY_DIR.is_dir():
        return dirs
    for year_path in sorted(DAILY_DIR.iterdir(), reverse=reverse):
        if not year_path.is_dir():
            continue
        for month_path in sorted(year_path.iterdir(), reverse=reverse):
            if not month_path.is_dir():
                continue
            for day_path in sorted(month_path.iterdir(), reverse=reverse):
                if day_path.is_dir() and (day_path / "problems.md").exists():
                    dirs.append(day_path)
    return dirs


def scan_unchecked(username: str, limit: int = 5) -> list[dict]:
    results = []
    for day_dir in get_date_dirs(reverse=True):
        problems = parse_problems_md(day_dir / "problems.md")
        for p in problems:
            if check_submission(day_dir, p["file_code"], username):
                continue
            rel = day_dir.relative_to(DAILY_DIR)
            date_str = rel.name
            results.append(
                {
                    "date": date_str,
                    "year": rel.parent.parent.name,
                    "month": rel.parent.name,
                    "difficulty": p["difficulty"],
                    "code": p["code"],
                    "file_code": p["file_code"],
                    "url": p["url"],
                    "hint": p["hint"],
                }
            )
            if len(results) >= limit:
                return results
    return results


@app.route("/favicon.png")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "assets"), "siteLogo.png"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/unchecked")
def api_unchecked():
    username = request.args.get("username", "Meguhine").strip()
    limit = int(request.args.get("limit", 5))
    if not username:
        return jsonify({"error": "username is required"}), 400
    problems = scan_unchecked(username, limit)
    return jsonify({"username": username, "count": len(problems), "problems": problems})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
