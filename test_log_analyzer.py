import unittest

from log_analyzer import analyze

SAMPLE = [
    '1.1.1.1 - - [28/Oct/2026:10:00:00 +0300] "GET /index.html?x=1 HTTP/1.1" 200 512 "-" "curl"',
    '1.1.1.1 - - [28/Oct/2026:10:00:01 +0300] "GET /index.html HTTP/1.1" 200 512 "-" "curl"',
    '2.2.2.2 - - [28/Oct/2026:10:00:02 +0300] "GET /missing HTTP/1.1" 404 0 "-" "curl"',
    '3.3.3.3 - - [28/Oct/2026:10:00:03 +0300] "POST /api HTTP/1.1" 500 0 "-" "curl"',
    "это не строка лога",
]


class AnalyzerTest(unittest.TestCase):
    def test_counts_and_percentages(self):
        r = analyze(SAMPLE, top=2)
        self.assertEqual(r["total"], 4)
        self.assertEqual(r["errors_4xx_pct"], 25.0)
        self.assertEqual(r["errors_5xx_pct"], 25.0)
        self.assertEqual(r["top_paths"][0], ("/index.html", 2))  # query string отброшена
        self.assertEqual(r["top_ips"][0], ("1.1.1.1", 2))

    def test_empty_input(self):
        self.assertEqual(analyze([])["total"], 0)


if __name__ == "__main__":
    unittest.main()
