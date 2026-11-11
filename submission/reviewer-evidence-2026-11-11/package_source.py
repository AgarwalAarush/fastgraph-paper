"""Package this draft's source without altering historical submission bundles."""
from pathlib import Path
import re
import zipfile


packet = Path(__file__).resolve().parent
root = packet.parents[1]
files = [root / name for name in ("Paper.tex", "Paper.bbl", "references.bib")]
for name in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", (root / "Paper.tex").read_text()):
    path = root / "media" / name
    if not path.suffix:
        path = path.with_suffix(".pdf")
    assert path.is_file(), path
    files.append(path)
output = packet / "FastGraph-reviewer-evidence-source.zip"
with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(set(files)):
        archive.write(path, path.relative_to(root))
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
print(output, len(set(files)), "source files; archive integrity passed")
