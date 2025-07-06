#!/usr/bin/env python3

import panflute as pf
import requests
import re
import os
import sys
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

dois = set()
user_bib_path = None
merged_bib_path = None

# Set cache root from environment or default
CACHE_ROOT = Path(os.environ.get("PANDOC_CITATION_CACHE_DIR", Path.home() / ".pandoc_citation_cache"))

ARXIV_PATTERN = re.compile(r'^arxiv:(\d{4}\.\d{4,5}(v\d+)?)$', re.IGNORECASE)
DOI_PATTERN = re.compile(r'^doi:(10\.\d{4,9}/[-._;()/:A-Z0-9]+)$', re.IGNORECASE)

def fetch_arxiv_bibtex(arxivid):
  url = f"https://arxiv.org/bibtex/{arxivid}"
  resp = requests.get(url)
  if resp.status_code != 200:
    return None
  return resp.text.strip()

def fetch_doi_bibtex(doi):
  headers = {"Accept": "application/x-bibtex"}
  resp = requests.get(f"https://doi.org/{doi}", headers=headers)
  if resp.status_code != 200:
    return None
  return resp.text.strip()

def fetch_bibtex(key):
  if key.startswith("doi:"):
    kind = "doi"
    val = key[4:]
    fetch_func = fetch_doi_bibtex
  elif key.startswith("arxiv:"):
    kind = "arxiv"
    val = key[6:]
    fetch_func = fetch_arxiv_bibtex
  else:
    return None

  safe_path = quote(val, safe="")
  cache_path = CACHE_ROOT / kind / (safe_path + ".bib")

  if cache_path.exists():
    return cache_path.read_text()

  bib = fetch_func(val)
  if not bib:
    return None

  cache_path.parent.mkdir(parents=True, exist_ok=True)
  cache_path.write_text(bib)
  return bib

def fetch_and_format(key):
  bib = fetch_bibtex(key)
  if not bib:
    return None
  # Replace key but keep entry type
  return re.sub(r"@(\w+)\{[^,]+", f"@\\1{{{key}", bib, 1)

def parse_existing_bib(bib_path):
  entries = []
  with open(bib_path) as f:
    content = f.read()
    raw_entries = re.split(r'(?=@\w+\{)', content)
    for entry in raw_entries:
      if entry.strip():
        entries.append(entry.strip())
  return entries

def action(elem, doc):
  if isinstance(elem, pf.Cite):
    for c in elem.citations:
      cid = c.id.lower()
      if cid.startswith("doi:") or cid.startswith("arxiv:"):
        dois.add(cid)
        c.id = cid.lower()

def prepare(doc):
  global user_bib_path
  meta = doc.get_metadata()

  bib = meta.get('bibliography')
  if isinstance(bib, list):
    user_bib_path = bib[0]
  elif isinstance(bib, str):
    user_bib_path = bib

  if meta.get("clear-cache") is True:
    if CACHE_ROOT.exists():
      shutil.rmtree(CACHE_ROOT)

def finalize(doc):
  global merged_bib_path
  merged = []

  if user_bib_path and Path(user_bib_path).exists():
    merged.extend(parse_existing_bib(user_bib_path))

  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(fetch_and_format, key): key for key in dois}
    for future in as_completed(futures):
      result = future.result()
      if result:
        merged.append(result)

  with NamedTemporaryFile(mode='w+', suffix='.bib', delete=False) as tmp:
    tmp.write("\n\n".join(merged))
    merged_bib_path = tmp.name

  doc.metadata['bibliography'] = pf.MetaList(pf.MetaString(merged_bib_path))

def main(doc=None):
  return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)

if __name__ == "__main__":
  main()
