#!/usr/bin/env python3
"""
Facebook App Scraper
--------------------
Scrapes active and inactive applications authorized on a Facebook account.

API Developer: SHAH MAKHDUM SHAJON
GitHub: SHAJON-404
Telegram: https://t.me/SHAJON404_OFFICIAL
"""

import json
import re
from typing import Dict, Any, Optional, List
import requests
from bs4 import BeautifulSoup

class FacebookAppScraper:
    """Scraper to retrieve active and inactive Facebook connected apps using user cookies."""
    
    BASE_URL: str = "https://m.facebook.com"

    def __init__(self, cookies: str) -> None:
        self.cookies: str = cookies.strip()
        self.status: str = "Live"
        self.session: requests.Session = requests.Session()
        self.session.headers.update({
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9,bn-BD;q=0.8,bn;q=0.7',
            'cache-control': 'no-cache, no-store, must-revalidate',
            'cookie': self.cookies,
            'dpr': '2.9',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
            'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6961.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': 'Linux',
            'sec-ch-ua-platform-version': '""',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'viewport-width': '980',
            'pragma': 'no-cache',
            'expires': '0'
        })
        self.active_apps: Dict[str, str] = {}
        self.inactive_apps: Dict[str, str] = {}

    def _clean_date(self, date_info: str) -> str:
        """Cleans and formats the raw Facebook date string."""
        return date_info.replace("Added on ", "").strip()

    def _scrape_tab(self, url: str, app_type: str) -> None:
        """Recursively scrapes the tabbed apps pages."""
        full_url: str = f"{self.BASE_URL}{url}"
        
        try:
            response = self.session.get(full_url, timeout=15)
            response.raise_for_status()
        except requests.RequestException:
            # Handle request failures gracefully
            self.status = "Expired"
            return

        if "Log Into Facebook" in response.text:
            # Invalid/expired cookies, stop parsing
            self.status = "Expired"
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        apps_dict = self.active_apps if app_type == "active_apps" else self.inactive_apps

        for div in soup.find_all("div", class_="_1yxq c"):
            name_tag = div.find("span", class_="_1yyi _9dut")
            date_tag = div.find("p", class_="_90gc mfss fcg")
            
            if name_tag and date_tag:
                app_name = name_tag.get_text(strip=True)
                date_info = date_tag.get_text(strip=True)
                apps_dict[app_name] = self._clean_date(date_info)

        see_more_div = soup.find("div", id="appsSectionSeeMoreApps")
        if see_more_div:
            a_tag = see_more_div.find("a", href=True)
            if a_tag:
                self._scrape_tab(a_tag["href"], app_type)

    def scrape(self) -> Dict[str, Any]:
        """Scrapes both active and inactive Facebook apps and returns a sorted dictionary."""
        if not self.cookies:
            return {
                "status": {
                    "cookie": "Dead",
                    "found_apps": False
                },
                "summary": {
                    "valid_apps": 0,
                    "invalid_apps": 0
                },
                "all_apps": {
                    "active_apps": None,
                    "inactive_apps": None
                }
            }

        self.active_apps.clear()
        self.inactive_apps.clear()
        self.status = "Live"

        # Scrape active and inactive applications
        self._scrape_tab("/settings/apps/tabbed/?tab=active", "active_apps")
        self._scrape_tab("/settings/apps/tabbed/?tab=inactive", "inactive_apps")

        if self.status == "Expired":
            return {
                "status": {
                    "cookie": "Dead",
                    "found_apps": False
                },
                "summary": {
                    "valid_apps": 0,
                    "invalid_apps": 0
                },
                "all_apps": {
                    "active_apps": None,
                    "inactive_apps": None
                }
            }

        # Sort the apps alphabetically by key
        sorted_active = dict(sorted(self.active_apps.items())) if self.active_apps else None
        sorted_inactive = dict(sorted(self.inactive_apps.items())) if self.inactive_apps else None

        valid_count = len(self.active_apps)
        invalid_count = len(self.inactive_apps)
        found_apps = (valid_count > 0 or invalid_count > 0)

        return {
            "status": {
                "cookie": "Live",
                "found_apps": found_apps
            },
            "summary": {
                "valid_apps": valid_count,
                "invalid_apps": invalid_count
            },
            "all_apps": {
                "active_apps": sorted_active,
                "inactive_apps": sorted_inactive
            }
        }

def extract_cookie(line: str) -> Optional[str]:
    """Auto-detects and extracts Facebook cookies containing 'datr=' and 'c_user=' from a line."""
    line = line.strip()
    if not line:
        return None

    # Check for '|' delimiter first
    if "|" in line:
        for part in line.split("|"):
            part_clean = part.strip()
            if "datr=" in part_clean and "c_user=" in part_clean:
                return part_clean

    # Check for ',' delimiter
    if "," in line:
        for part in line.split(","):
            part_clean = part.strip()
            if "datr=" in part_clean and "c_user=" in part_clean:
                return part_clean

    # If no delimiters match, check if the entire line is a cookie
    if "datr=" in line and "c_user=" in line:
        return line

    return None

def extract_uid(cookie: str) -> str:
    """Helper to extract c_user ID from the cookie string for display purposes."""
    match = re.search(r'c_user=(\d+)', cookie)
    return match.group(1) if match else "Unknown UID"

def main() -> None:
    print("-" * 80)
    print("Facebook Connected Apps Scraper".center(80))
    print("-" * 80)
    print("1. Input Cookies (Manual)")
    print("2. Import Cookies from File")
    print("-" * 80)

    choice = input("[+] Select an option (1/2): ").strip()
    print("-" * 80)

    cookies_list: List[str] = []

    if choice == "1":
        cookie_input = input("[+] Enter Facebook Cookies: ").strip()
        print("-" * 80)
        if not cookie_input:
            print("[-] Error: Cookies are required.")
            print("-" * 80)
            return

        if "datr=" not in cookie_input or "c_user=" not in cookie_input:
            print("[-] Error: Invalid cookie format. Must contain 'datr=' and 'c_user='.")
            print("-" * 80)
            return
        cookies_list.append(cookie_input)

    elif choice == "2":
        file_path = input("[+] Enter Cookie File Path: ").strip()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"[-] Error: File '{file_path}' not found.")
            print("-" * 80)
            return
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            print("-" * 80)
            return

        for line in lines:
            cookie = extract_cookie(line)
            if cookie:
                cookies_list.append(cookie)

        if not cookies_list:
            print("[-] Error: No valid cookies containing 'datr=' and 'c_user=' found in the file.")
            print("-" * 80)
            return

        print(f"[+] Found {len(cookies_list)} valid cookie(s) in the file.")
        print("-" * 80)
    else:
        print("[-] Error: Invalid option selected.")
        print("-" * 80)
        return

    # Process all cookies
    for idx, cookies in enumerate(cookies_list, 1):
        uid = extract_uid(cookies)
        if len(cookies_list) > 1:
            print(f"[+] [{idx}/{len(cookies_list)}] Scraping apps for UID: {uid}...")
        else:
            print(f"[+] Scraping apps for UID: {uid}...")

        scraper = FacebookAppScraper(cookies)
        result = scraper.scrape()

        print(f"[+] Result for UID {uid}:")
        print("-" * 80)
        print(json.dumps(result, indent=4, ensure_ascii=False))
        print("-" * 80)

if __name__ == "__main__":
    main()
