import requests
from api.models import Location
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import data from API'

    def handle(self, *args, **options):
        # Initialize variables
        base_url = "https://api.openaq.org/v2/locations?limit=1000&offset=0&sort=desc&radius=1000&order_by=lastUpdated&dump_raw=false"
        page = 1
        headers = {"accept": "application/json",
                   "X-API-Key": "47ef3bf63537c3d0687ce523ad910cdb30eda1f78fe0d81429fccb8a2af10ec6"}

        while True:
            # Make a request to the API for the current page
            params = {"page": page}
            response = requests.get(base_url, params=params, headers=headers)

            if response.status_code == 200:
                # Extract the data from the current page
                current_page_data = response.json()

                # Extract the meta information from the current page
                meta = current_page_data.get("meta", {})

                # Check if there are more pages to fetch
                if meta.get("page", 0) * meta.get("limit", 0) >= meta.get("found", 0):
                    break
                
                for item in current_page_data.get("results"):
                    location = Location()
                    location.location_id = item["id"]
                    location.country = item["country"]
                    location.city = item["city"]
                    location.name = item["name"]
                    location.save()

                self.stdout.write(self.style.SUCCESS(f'Data imported successfully from page {page}'))
                # Increment the page number for the next request
                page += 1
            else:
                self.stdout.write(self.style.ERROR(f"Request failed with status code: {response.status_code}"))
                break

