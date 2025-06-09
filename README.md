# pandoc-smart-cite

A Pandoc filter that automatically resolves `@doi:` and `@arxiv:` citations by fetching BibTeX metadata from official sources and integrating them seamlessly into your Pandoc citation workflow.

---

## ✨ Features

- 📚 Supports `@doi:10.1126/science.abn6697` and `@arxiv:0706.0001v1`
- ⚡ Parallel BibTeX fetching
- 💾 Persistent local cache (`~/.pandoc_citation_cache` or `$PANDOC_CITATION_CACHE_DIR`)
- 🧠 Merges with user `--bibliography`
- 🔁 Respects original BibTeX entry type (`@article`, `@misc`, etc.)
- 📦 Installable via `pip`

---

## 📦 Installation

```bash
pip install git+https://github.com/mgravey/pandoc-smart-cite.git
````

---

## 🚀 Usage

### With Pandoc

```bash
pandoc input.md \
	--filter=smart-cite.py \
	--citeproc \
	--bibliography=mylibrary.bib \
	--csl=apa.csl \
	-o output.pdf
```

### Clear Cache

```bash
pandoc input.md \
	--filter=smart-cite.py \
	--metadata=clear-cache:true \
	--citeproc \
	--bibliography=mylibrary.bib \
	-o output.pdf
```

### Custom Cache Directory

```bash
PANDOC_CITATION_CACHE_DIR=./cache pandoc ...
```

---

## 🔧 Supported Citation Keys

| Type  | Syntax Example                   |
| ----- | -------------------------------- |
| DOI   | `[@doi:10.1126/science.abn6697]` |
| arXiv | `[@arxiv:0706.0001v1]`           |

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

* [Panflute](https://github.com/sergiocorreia/panflute)
* [Crossref](https://www.crossref.org/)
* [arXiv](https://arxiv.org/)
* [Pandoc](https://pandoc.org)