"""Анализ access-лога веб-сервера (формат combined, nginx/Apache).
Запуск: python log_analyzer.py access.log [--top 5]
Показывает: число запросов, долю ошибок 5xx/4xx, топ страниц и топ IP.
"""
import argparse
import collections
import re

LINE = re.compile(r'^(\S+) \S+ \S+ \[[^\]]+\] "(?:\S+) (\S+)[^"]*" (\d{3}) ')


def parse(lines):
    """Генератор (ip, path, status); битые строки пропускаются."""
    for line in lines:
        m = LINE.match(line)
        if m:
            ip, path, status = m.groups()
            yield ip, path.split("?")[0], int(status)


def analyze(lines, top=5):
    paths, ips, classes = collections.Counter(), collections.Counter(), collections.Counter()
    total = 0
    for ip, path, status in parse(lines):
        total += 1
        paths[path] += 1
        ips[ip] += 1
        classes[status // 100] += 1
    pct = lambda n: round(100 * n / total, 1) if total else 0.0
    return {
        "total": total,
        "errors_4xx_pct": pct(classes[4]),
        "errors_5xx_pct": pct(classes[5]),
        "top_paths": paths.most_common(top),
        "top_ips": ips.most_common(top),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("logfile")
    p.add_argument("--top", type=int, default=5)
    args = p.parse_args()
    with open(args.logfile, encoding="utf-8", errors="replace") as f:
        r = analyze(f, args.top)
    print(f"Запросов: {r['total']}  4xx: {r['errors_4xx_pct']}%  5xx: {r['errors_5xx_pct']}%")
    print("Топ страниц:")
    for path, n in r["top_paths"]:
        print(f"  {n:>6}  {path}")
    print("Топ IP:")
    for ip, n in r["top_ips"]:
        print(f"  {n:>6}  {ip}")


if __name__ == "__main__":
    main()
