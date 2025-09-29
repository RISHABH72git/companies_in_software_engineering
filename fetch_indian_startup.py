import pandas as pd
import httpx

API_URL = "https://api.startupindia.gov.in/sih/api/noauth/search/profiles"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.startupindia.gov.in/",
    "Origin": "https://www.startupindia.gov.in",
    "Content-Type": "application/json"
}
base_payload = {
    "query": "",
    "focusSector": False,
    "industries": [],
    "sectors": [],
    "states": [],
    "cities": [],
    "stages": ["scaling"],
    "badges": [],
    "roles": ["Startup"],
    "page": 0,
    "sort": {
        "orders": [{"field": "registeredOn", "direction": "DESC"}]
    },
    "dpiitRecogniseUser": False,
    "internationalUser": False
}


def fetch_page_data(client, page_number):
    payload = base_payload.copy()
    payload["page"] = page_number
    try:
        print("Fetching page {}".format(page_number))
        response = client.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        print(f"Request error on page {page_number}: {e}")
        return {}


def gather_all_data(max_pages=20):
    all_data = []
    for i in range(max_pages):
        with httpx.Client(timeout=30) as client:
            results = fetch_page_data(client, i)
            if "content" in results:
                all_data.extend(results["content"])

    return pd.DataFrame(all_data)


# Run this to fetch data and save
if __name__ == "__main__":
    df = gather_all_data(max_pages=5000)  # Adjust max_pages as needed
    df.to_csv("startup_india_profiles.csv", index=False)
    print(f"Saved {len(df)} startup profiles to 'startup_india_profiles.csv'")
