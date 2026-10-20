import requests
from datetime import datetime, timezone

# 源地址
SRC_URL = "https://deepformat.top/yh/fake.txt"
OUTPUT_FILE = "filter.txt"

# 头部模板（和你截图样式一致）
HEADER = """! Title: fake filters - Badware risks
! Description: Auto generated from deepformat.top/yh/fake.txt
! Version: 1.0.0.{unixtime}
! Homepage: https://github.com/{repo_owner}/{repo_name}
! Last modified: {now}
! Compiled by GitHub Actions
!
"""

def main():
    # 拉取源文本
    resp = requests.get(SRC_URL, timeout=30)
    resp.raise_for_status()
    lines = resp.text.splitlines()

    rules = []
    for line in lines:
        d = line.strip()
        # 跳过空行、注释行
        if not d or d.startswith("#") or d.startswith("!"):
            continue
        rules.append(f"||{d}^")

    # 去重 + 排序
    rules = sorted(list(set(rules)))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    import os
    repo_full = os.getenv("GITHUB_REPOSITORY", "user/repo")
    owner, repo = repo_full.split("/")
    unixtime = int(datetime.now().timestamp())

    header = HEADER.format(
        now=now,
        repo_owner=owner,
        repo_name=repo,
        unixtime=unixtime
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(rules))
        f.write("\n")
    print(f"✅ 生成 {OUTPUT_FILE}，共 {len(rules)} 条规则")

if __name__ == "__main__":
    main()
