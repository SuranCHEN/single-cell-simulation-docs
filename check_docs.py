"""Read-only checks for the documentation package; never runs simulations."""
import csv
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parent
pages = ("index", "model", "settings", "evaluation", "history", "sources")
for name in pages:
    path = root / (name + ".md")
    text = path.read_text()
    assert text.startswith("---\n"), path
    assert f"slug: {name}\n" in text, path
    assert text.count("$$") % 2 == 0, path
    for target in re.findall(r"\]\(([^)]+)\)", text):
        url = urlsplit(target)
        if not url.scheme and url.path:
            assert (path.parent / unquote(url.path)).is_file(), (path, target)

evidence = root / "evidence"
read = lambda name: json.loads((evidence / name).read_text())
for row in read("source-manifest.json")["files"]:
    if row["published_file"]:
        actual = hashlib.sha256((evidence / row["published_file"]).read_bytes()).hexdigest()
        assert actual == row["published_sha256"], row["published_file"]

depth = read("depth-20260910.json")
assert depth["n_gwas"] == 20000
assert depth["simulation"]["cell_variance"] == 8
assert depth["simulation"]["donor_variance"] == .8
assert depth["target_cells_per_donor"] == [10, 50, 200, 1000]
confirm = read("confirmation.json")
assert confirm["donor_n"] == 500 and confirm["target_cells"] == 1000
assert confirm["expected_shared"] + confirm["expected_negative"] == 1950
assert len(confirm["centers"]) == 6
with (evidence / "confirmation-summary.tsv").open() as f:
    rows = {r["method"]: r for r in csv.DictReader(f, delimiter="\t")}
assert int(rows["CLike_dimension"]["negative_filtered"]) - int(rows["original_CLike"]["negative_filtered"]) == 199
assert int(rows["CLike_dimension"]["shared_lost"]) - int(rows["original_CLike"]["shared_lost"]) == 1
for path in root.rglob("*"):
    if path.is_file() and ".git" not in path.parts and path.name not in {"check_docs.py", ".DS_Store"}:
        text = path.read_text()
        assert "/Users/" not in text, path
        assert not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}", text), path
print("PASS: 6 Markdown pages, internal file links, equations, evidence hashes, settings and aggregate counts")
