import json
from api import fetch_and_convert

def main():
    api_url = "https://sample.xtrascale.com/api.php"
    results = fetch_and_convert(api_url)
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
