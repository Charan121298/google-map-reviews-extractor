# Google Map Reviews Extractor

## Overview

The Google Map Reviews Extractor is a Python-based tool designed to scrape and analyze reviews from Google Maps. This project leverages the power of web scraping to gather user reviews for businesses, restaurants, attractions, and more from Google Maps, allowing users to collect data for various purposes such as sentiment analysis, market research, and business intelligence.

## Features

- Extract reviews from Google Maps for any given place.
- Gather details like review text, rating, date, reviewer name, and more.
- Save extracted reviews to CSV.
- Simple and easy-to-use command-line interface.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- Required Python packages listed in `requirements.txt`.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Charan121298/google-map-reviews-extractor.git
    ```

2. Change to the project directory:

    ```sh
    cd google-map-reviews-extractor
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Basic Usage

To run the extractor with basic settings, use the following command:

```sh
python main.py --place "google-map-url"
