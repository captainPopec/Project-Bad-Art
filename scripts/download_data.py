"""
Download ~210 biophony and ~200 anthropophony samples from Freesound.
Saves WAV files to ../data/bio/ and ../data/antropo/, trimmed to 60s for standardization of inputs, 
also all files are of same quality
Writes ../data/metadata.csv. Skips already-downloaded files.
"""

import os
import time
import csv
import requests
import subprocess
import tempfile

FREESOUND_API_KEY = "vDb59opEpktBxoeCzPtIn0aa3oqLEozzeR066r9j"
BASE_URL = "https://freesound.org/apiv2/search/text/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
BIO_DIR = os.path.join(DATA_DIR, "bio")
ANTROPO_DIR = os.path.join(DATA_DIR, "antropo")
METADATA_CSV = os.path.join(DATA_DIR, "metadata.csv")
DURATION_FILTER = "duration:[180 TO 1200]"
TARGET_DURATION_S = 60
FFMPEG = "/g/stegle/spiljak/programs/miniforge3/envs/bad-art/bin/ffmpeg"

BIO_QUERIES = [
    ("forest soundscape", 36),
    ("tropical rainforest ambience", 36),
    ("ocean waves nature", 35),
    ("wetland birds dawn chorus", 35),
    ("grassland insects nature", 35),
    ("river stream nature ambience", 33),
]

ANTROPO_QUERIES = [
    ("city traffic urban noise", 41),
    ("industrial machinery factory", 40),
    ("crowd noise people talking", 40),
    ("construction site noise", 40),
    ("highway road traffic", 39),
]


def freesound_search(query, page_size=150):
    params = {
        "query": query,
        "filter": DURATION_FILTER,
        "fields": "id,name,previews,duration,tags",
        "page_size": page_size,
        "token": FREESOUND_API_KEY,
    }
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("results", [])


def download_and_trim(preview_url, out_path):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        r = requests.get(preview_url, timeout=60, stream=True)
        r.raise_for_status()
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                f.write(chunk)

        cmd = [
            FFMPEG, "-y", "-i", tmp_path,
            "-t", str(TARGET_DURATION_S),
            "-ar", "44100", "-ac", "1",
            "-acodec", "pcm_s16le",
            out_path,
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=120)
        return result.returncode == 0
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def collect_samples(queries, out_dir, group_label, existing_ids, metadata_rows):
    os.makedirs(out_dir, exist_ok=True)
    downloaded = 0
    total_target = sum(n for _, n in queries)

    for query, target in queries:
        print(f"\n  Query: '{query}' (want {target})")
        try:
            results = freesound_search(query, page_size=min(150, target * 3))
        except Exception as e:
            print(f"    Search failed: {e}")
            continue

        count_for_query = 0
        for sound in results:
            if count_for_query >= target:
                break
            sid = str(sound["id"])
            if sid in existing_ids:
                continue
            preview = sound.get("previews", {}).get("preview-hq-mp3")
            if not preview:
                continue

            safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in sound["name"])
            fname = f"{sid}_{safe_name[:60]}.wav"
            out_path = os.path.join(out_dir, fname)

            if os.path.exists(out_path):
                existing_ids.add(sid)
                count_for_query += 1
                downloaded += 1
                continue

            print(f"    [{downloaded+1}/{total_target}] {sound['name'][:50]} ({sound['duration']:.0f}s)")
            try:
                ok = download_and_trim(preview, out_path)
                if ok:
                    existing_ids.add(sid)
                    metadata_rows.append({
                        "id": sid,
                        "group": group_label,
                        "query": query,
                        "name": sound["name"],
                        "duration_orig": sound["duration"],
                        "filename": fname,
                    })
                    count_for_query += 1
                    downloaded += 1
                else:
                    print(f"      ffmpeg failed, skipping")
            except Exception as e:
                print(f"      Error: {e}")
            time.sleep(0.3)

        print(f"    Got {count_for_query}/{target} for this query")

    return downloaded


def load_existing_metadata():
    existing_ids = set()
    rows = []
    if os.path.exists(METADATA_CSV):
        with open(METADATA_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row["id"])
                rows.append(row)
    return existing_ids, rows


def save_metadata(rows):
    fieldnames = ["id", "group", "query", "name", "duration_orig", "filename"]
    with open(METADATA_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    existing_ids, metadata_rows = load_existing_metadata()
    print(f"Already have {len(existing_ids)} samples in metadata.")

    print("\n=== Downloading BIOPHONY samples ===")
    n_bio = collect_samples(BIO_QUERIES, BIO_DIR, "bio", existing_ids, metadata_rows)

    print("\n=== Downloading ANTHROPOPHONY samples ===")
    n_ant = collect_samples(ANTROPO_QUERIES, ANTROPO_DIR, "antropo", existing_ids, metadata_rows)

    save_metadata(metadata_rows)
    bio_total = len([r for r in metadata_rows if r["group"] == "bio"])
    ant_total = len([r for r in metadata_rows if r["group"] == "antropo"])
    print(f"\nDone. Bio: {bio_total}, Antropo: {ant_total}. Metadata: {METADATA_CSV}")


if __name__ == "__main__":
    main()
