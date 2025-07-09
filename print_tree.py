import os
import fnmatch

def parse_gitignore(path=".gitignore"):
    patterns = []
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                patterns.append(line)
    return patterns

def is_ignored(path, ignore_patterns):
    for pattern in ignore_patterns:
        # 디렉토리 패턴: "venv/" 같은 경우
        if pattern.endswith("/"):
            if os.path.isdir(path) and fnmatch.fnmatch(os.path.basename(path) + "/", pattern):
                return True
            # 하위 디렉터리 포함 무시
            if pattern[:-1] in path.replace("\\", "/").split("/"):
                return True
        # 파일/글로벌 패턴
        if fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def print_tree(root, prefix="", ignore_patterns=None):
    if ignore_patterns is None:
        ignore_patterns = []
    entries = [e for e in os.listdir(root) if not is_ignored(os.path.join(root, e), ignore_patterns)]
    entries.sort()
    for i, entry in enumerate(entries):
        path = os.path.join(root, entry)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)
        if os.path.isdir(path):
            next_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(path, next_prefix, ignore_patterns)

if __name__ == "__main__":
    IGNORE_PATTERNS = parse_gitignore(".gitignore")
    IGNORE_PATTERNS += [".git/"]  # 항상 .git 디렉터리는 무시
    print(".")
    print_tree(".", ignore_patterns=IGNORE_PATTERNS)
