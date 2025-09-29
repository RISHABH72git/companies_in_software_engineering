import re

import pandas as pd
import requests
import json

HR_KEYWORDS = ["hr", "humanresources", "careers", "jobs", "recruit", "talent", "people", "recruitment"]
SERPER_API_KEY = ' '  # set this in your env


def scrape_serper(search_url):
    url = "https://scrape.serper.dev"
    payload = json.dumps({
        "url": search_url
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def extract_emails(text: str) -> list[str]:
    # Standard email regex pattern
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, text)


def scan_domain(domain, deep_follow=False):
    text_response = scrape_serper(domain)
    emails = extract_emails(text_response)
    print(f"found {emails} emails from {domain}")
    return emails


def collect(domains, deep_follow=False):
    summary = []
    for d in domains:
        try:
            d_clean = d.strip()
            if not d_clean:
                continue
            print(f"[+] Scanning domain: {d_clean}")
            result = scan_domain(d_clean, deep_follow=deep_follow)
            summary.append({
                "career_url": d_clean,
                "emails": result
            })
        except Exception as e:
            print(f"error occurred in {d} {e}")
    return summary


def main():
    companies = pd.read_csv("companies_name_urls.csv", index_col=0)
    # Safely extract domain only if URL is a string
    domain_list = companies['career_url'].tolist()
    results = collect(domain_list, deep_follow=True)
    pd.DataFrame(results).to_csv("result_with_urls.csv", index=False)
    print(f"\nDone. Results written")


if __name__ == '__main__':
    main()
