# Facebook Connected Apps Scraper

A modern, object-oriented Python scraper designed to retrieve active and inactive applications authorized on a Facebook account.

**File Location:** [check-facebook-apps.py](file:///d:/GitHub-Projects/open-source/py-scripts/check-facebook-apps.py)

---

## ✨ Features
- **Object-Oriented Design:** Built using clean Python OOP principles with full type-hinting.
- **Auto-Detection Cookie Parser:** Automatically extracts cookies from various line formats in files:
  - `uid|password|cookie`
  - `uid,password,cookie`
  - Raw cookie strings (`datr=...; c_user=...;`)
- **Pagination Support:** Automatically follows "See More Apps" pagination to scrape all authorized applications.
- **Detailed JSON Responses:** Returns structured outputs containing:
  - `status`: Cookie validity (`"cookie": "Live" | "Dead"`) and whether applications were found (`"found_apps": true | false`).
  - `summary`: Total counts of active (`valid_apps`) and inactive (`invalid_apps`) applications.
  - `all_apps`: Lists of active and inactive applications (returns `null` if none found).
- **Session Re-use:** Uses `requests.Session` to optimize network requests and connection pooling.

---

## 🚀 Getting Started

### Dependencies
Ensure you have the required libraries installed:
```bash
pip install requests beautifulsoup4
```

### How to Run
Run the script using Python:
```bash
python py-scripts/check-facebook-apps.py
```

### How to Use
Upon execution, you will see an interactive menu:
1. **Input Cookies (Manual):** Paste a single raw Facebook cookie string.
2. **Import Cookies from File:** Provide a file path containing cookies. Each line of the file can be a raw cookie or delimited by pipe/comma (e.g., `uid|pass|cookies`).