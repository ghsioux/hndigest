import glob
import re

counts = {"Top Stories": [], "Projects & Tools": [], "Worth Reading": [], "Community Pulse": []}

for file in glob.glob("digests/*.md"):
    with open(file, "r") as f:
        content = f.read()
        
    sections = re.split(r'## ', content)
    for section in sections[1:]:
        lines = section.strip().split('\n')
        name = lines[0].strip()
        
        if "Top Stories" in name:
            items = len(re.findall(r'### ', section))
            counts["Top Stories"].append(items)
        elif "Projects & Tools" in name:
            items = len(re.findall(r'- \*\*', section))
            counts["Projects & Tools"].append(items)
        elif "Worth Reading" in name:
            items = len(re.findall(r'- \*\*', section))
            counts["Worth Reading"].append(items)
        elif "Community Pulse" in name:
            items = len(re.findall(r'- \*\*', section))
            counts["Community Pulse"].append(items)

for name, c in counts.items():
    if c:
        avg = sum(c)/len(c)
        min_c, max_c = min(c), max(c)
        print(f"{name}: avg {avg:.1f}, range {min_c}-{max_c}")
