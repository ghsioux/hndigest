import urllib.request
import json
import random

manifest_url = "https://news.msl.cloud/digests/manifest.json"
req = urllib.request.urlopen(manifest_url)
dates = json.loads(req.read())

random.seed(42) # for reproducibility
selected_dates = sorted(random.sample(dates, min(30, len(dates))))

print(f"Selected dates: {selected_dates}")

import os
os.makedirs("digests", exist_ok=True)

for date in selected_dates:
    url = f"https://news.msl.cloud/digests/{date}.md"
    try:
        content = urllib.request.urlopen(url).read().decode('utf-8')
        with open(f"digests/{date}.md", "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Failed to fetch {date}: {e}")

print("Done fetching")
