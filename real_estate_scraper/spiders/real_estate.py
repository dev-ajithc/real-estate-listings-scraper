import re
from datetime import datetime, timezone

import scrapy

from real_estate_scraper.items import PropertyItem


class RealEstateSpider(scrapy.Spider):
    name = "real_estate"

    allowed_domains = [
        "scrapifydatalabs.com",
    ]

    start_urls = [
        "https://scrapifydatalabs.com/playground/nestly/"
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    def parse(self, response):
        """
        Extract property listings from the Nestly search page.
        """

        cards = response.css(
            "article.nl-card[data-home-id]"
        )

        for card in cards:
            listing_id = card.attrib.get("data-home-id")

            price = card.css(
                ".nl-price::attr(data-price)"
            ).get()

            title = card.css(
                "a::attr(aria-label)"
            ).get()

            if not title:
                title = card.css(
                    "h2::text"
                ).get()

            address = card.css(
                ".nl-address::text"
            ).get()

            listing_url = card.css(
                "a::attr(href)"
            ).get()

            listing_url = response.urljoin(
                listing_url
            ) if listing_url else None

            text = " ".join(
                card.css("*::text").getall()
            )

            bedrooms = self.extract_number(
                text,
                r"(\d+)\s*bds?"
            )

            bathrooms = self.extract_number(
                text,
                r"([\d.]+)\s*ba"
            )

            area_sqft = self.extract_number(
                text,
                r"([\d,]+)\s*sqft"
            )

            property_type = self.extract_property_type(
                text
            )

            status = self.extract_status(
                text
            )

            price_period = (
                "monthly"
                if "/mo" in text.lower()
                else "sale"
            )

            agent = self.extract_agent(
                text
            )

            yield PropertyItem(
                listing_id=listing_id,
                title=self.clean_text(title),
                status=status,
                price=self.clean_price(price),
                price_period=price_period,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                area_sqft=area_sqft,
                property_type=property_type,
                address=self.clean_text(address),
                city="Austin",
                postal_code=self.extract_postal_code(
                    address
                ),
                agent=agent,
                listing_url=listing_url,
                scraped_at=datetime.now(
                    timezone.utc
                ).isoformat(),
            )

    @staticmethod
    def clean_text(value):
        if not value:
            return None

        return " ".join(value.split()).strip()

    @staticmethod
    def clean_price(value):
        if not value:
            return None

        value = re.sub(
            r"[^\d.]",
            "",
            value
        )

        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def extract_number(text, pattern):
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if not match:
            return None

        value = match.group(1).replace(",", "")

        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def extract_postal_code(address):
        if not address:
            return None

        match = re.search(
            r"\b\d{5}\b",
            address
        )

        return match.group(0) if match else None

    @staticmethod
    def extract_status(text):
        text_lower = text.lower()

        if "pending" in text_lower:
            return "pending"

        if "for rent" in text_lower:
            return "rent"

        if "for sale" in text_lower:
            return "sale"

        return None

    @staticmethod
    def extract_property_type(text):
        text_lower = text.lower()

        property_types = {
            "single family": "single_family",
            "condo": "condo",
            "townhouse": "townhouse",
            "multi family": "multi_family",
            "apartment": "apartment",
            "manufactured": "manufactured",
        }

        for source, normalized in property_types.items():
            if source in text_lower:
                return normalized

        return None

    @staticmethod
    def extract_agent(text):
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return None

        return lines[-1]
