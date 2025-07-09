# [PATH] test.py

import os
import re

BASE_DIR = "/mnt/d/Project/Game-Stream-Trends"

COMMENT_STYLES = {
    ".py": "#",
    ".sh": "#",
    ".yaml": "#",
    ".yml": "#",
    ".toml": "#",
    ".ini": "#",
    ".conf": "#",
    ".env": "#",
    ".js": "//",
    ".ts": "//",
    ".go": "//",
    ".java": "//",
    ".c": "//",
    ".cpp": "//",
    ".sql": "--",
    ".dockerfile": "#",
    ".html": "<!--",
    ".htm": "<!--",
    ".css": "/*",
}

SKIP_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".zip", ".tar", ".gz", ".exe", ".pdf", ".db"]

def make_path_comment(rel_path, comment_style):
    if comment_style == "<!--":
        return f"<!-- [PATH] {rel_path} -->\n"
    elif comment_style == "/*":
        return f"/* [PATH] {rel_path} */\n"
    else:
        return f"{comment_style} [PATH] {rel_path}\n"

def is_path_comment(line):
    return "[PATH]" in line

def extract_path_from_comment(line):
    match = re.search(r"\[PATH\]\s+(.+)", line)
    if match:
        return match.group(1).strip()
    return ""

for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in [".git", ".venv", "__pycache__"]]
    for filename in files:
        file_path = os.path.join(root, filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext in SKIP_EXTS:
            continue
        rel_path = os.path.relpath(file_path, BASE_DIR).replace("\\", "/")
        comment_style = COMMENT_STYLES.get(ext, "#")
        new_comment = make_path_comment(rel_path, comment_style)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            print(f"[skip] 인코딩 문제로 건너뜀: {file_path}")
            continue

        # 이미 최상단에 [PATH] 주석이 있는 경우, 실제 현재 경로와 일치하는지 비교
        if lines and is_path_comment(lines[0]):
            current_path = extract_path_from_comment(lines[0])
            if current_path == rel_path:
                # 경로 주석 아래가 빈 줄 아니면 빈 줄 추가
                if len(lines) < 2 or lines[1].strip() != "":
                    lines = [lines[0], '\n'] + lines[1:]
                # 아니면 그대로
            else:
                lines[0] = new_comment
                if len(lines) < 2 or lines[1].strip() != "":
                    lines = [lines[0], '\n'] + lines[1:]
        else:
            # 없으면 항상 맨 위에 추가 + 빈 줄
            lines = [new_comment, '\n'] + lines

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"✅ [ADD/UPDATE] {file_path}")

print("완료: 모든 파일의 경로 주석([PATH])을 최상단에 추가 + 한 칸 개행")
