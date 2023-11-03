import requests
from api.models import Location
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import data from API'

    def handle(self, *args, **options):
        # Initialize variables
        base_url = "https://api.openaq.org/v2/countries?limit=100&page=1&offset=0&sort=asc&order_by=name"

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

                # Check if the current page contains data
                if not current_page_data or not current_page_data.get("results"):
                    # No more data available, exit the loop
                    break

                for item in current_page_data.get("results"):
                    locations = Location.objects.filter(country=item["code"])
                    for location in locations:
                        location.country = item["name"]
                        location.save()

                self.stdout.write(self.style.SUCCESS(f'Data imported successfully from page {page}'))

                # Increment the page number for the next request
                page += 1
            else:
                self.stdout.write(self.style.ERROR(f"Request failed with status code: {response.status_code}"))
                break

