# Real Estate Listings Scraper & Data Cleaning Pipeline

A portfolio-ready real estate web scraping project built with Python and Scrapy.

The project extracts structured property listings from **Nestly**, a fictional Zillow-style real estate practice website created specifically for web-scraping practice. The target provides public listing cards and property details without requiring authentication.

## Project Overview

The pipeline demonstrates a practical real-estate data workflow:

- Property listing extraction
- Pagination / listing discovery
- Price normalization
- Bedroom, bathroom, and area parsing
- Property-type normalization
- Address extraction
- Listing URL normalization
- Duplicate detection
- Required-field validation
- CSV export
- Data-quality reporting

## Architecture

```text
Nestly Real Estate Practice Site
              |
              v
        Scrapy Spider
              |
              v
       Raw Listings CSV
              |
              v
      Data Normalization
              |
              v
       Deduplication
              |
              v
          Validation
              |
              v
      Clean Listings CSV
              |
              v
       Quality Report
```

## Data Fields

| Field | Description |
|---|---|
| listing_id | Unique listing identifier |
| title | Listing title |
| status | For sale / rent / pending |
| price | Numeric asking price |
| price_period | Sale price or monthly rent |
| bedrooms | Number of bedrooms |
| bathrooms | Number of bathrooms |
| area_sqft | Property area in square feet |
| property_type | Normalized property type |
| address | Property address |
| city | City |
| postal_code | Postal code |
| agent | Listing company / agent |
| listing_url | Property detail URL |
| scraped_at | UTC extraction timestamp |

## Tech Stack

- Python
- Scrapy
- Pandas
- CSS selectors
- CSV
- Data validation

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/real-estate-listings-scraper.git
cd real-estate-listings-scraper
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Scraper

```bash
scrapy crawl real_estate
```

Raw data will be written to:

```text
data/listings_raw.csv
```

## Clean and Normalize the Dataset

```bash
python real_estate_scraper/clean_data.py
```

Clean data will be written to:

```text
data/listings_clean.csv
```

## Generate the Data Quality Report

```bash
python reports/data_quality_report.py
```

The report will be generated at:

```text
reports/data_quality_report.md
```

## Data Quality Checks

The pipeline validates:

- Required listing fields
- Numeric price values
- Bedroom and bathroom values
- Property area
- Listing URLs
- Duplicate listing IDs
- Duplicate listing URLs
- Data completeness

The metrics in the generated report come from the actual scraper run and are not hard-coded.

## Portfolio Use Cases

This project demonstrates techniques applicable to:

- Real estate listing aggregation
- Rental market datasets
- Property price monitoring
- Housing market research
- Competitor listing analysis
- Real estate analytics
- Recurring property-data pipelines

## Responsible Scraping

Nestly is a fictional real-estate practice website designed for scraping exercises. Scraping is explicitly encouraged by the site for learning and demonstration purposes.

For production projects involving real websites, always review the target site's terms, robots directives, access requirements, and applicable laws before collecting data.

## Example Pipeline Output

```text
Raw listings
    ↓
Normalize price
    ↓
Normalize property type
    ↓
Parse bedrooms / bathrooms / area
    ↓
Normalize URLs
    ↓
Remove duplicates
    ↓
Validate required fields
    ↓
Export clean CSV
```
