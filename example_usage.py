#!/usr/bin/env python3
"""
Example usage of the Python CIMIS Client library.

This script demonstrates how to use the library to fetch weather data
and export it to CSV format.
"""

import os
from datetime import date, timedelta
from python_cimis import CimisClient, CimisAPIError, CimisAuthenticationError


def main():
    """Main example function."""
    
    # Initialize the client with your API key
    # You can get an API key from: https://cimis.water.ca.gov/Default.aspx
    api_key = os.environ.get('CIMIS_API_KEY')
    if not api_key:
        print("Please set the CIMIS_API_KEY environment variable")
        print("You can get an API key from: https://cimis.water.ca.gov/Default.aspx")
        return
    
    client = CimisClient(app_key=api_key)
    
    # Define date range (last 7 days)
    end_date = date.today() - timedelta(days=1)  # Yesterday
    start_date = end_date - timedelta(days=6)    # 7 days ago
    
    print(f"Fetching CIMIS data from {start_date} to {end_date}")
    
    try:
        # Example 1: Get daily weather data by station numbers
        print("\n1. Getting daily weather data by station numbers...")
        weather_data = client.get_daily_data(
            targets=[2, 8, 127],  # Station numbers
            start_date=start_date,
            end_date=end_date
            # unit_of_measure="M" is the default (Metric units)
        )
        
        # Export to CSV with all available columns
        print("   Exporting to 'station_weather_data.csv'...")
        client.export_to_csv(weather_data, "station_weather_data.csv")
        
        # Print summary
        all_records = weather_data.get_all_records()
        print(f"   Retrieved {len(all_records)} weather records")
        
        # Example 2: Get weather data by zip codes
        print("\n2. Getting weather data by zip codes...")
        zip_weather_data = client.get_daily_data(
            targets=["95823", "94503", "93624"],
            start_date=start_date,
            end_date=end_date,
            prioritize_scs=True  # Use Spatial CIMIS System when available
        )
        
        # Export to CSV
        print("   Exporting to 'zip_weather_data.csv'...")
        client.export_to_csv(zip_weather_data, "zip_weather_data.csv")
        
        # Example 3: Get station information
        print("\n3. Getting station information...")
        stations = client.get_stations()
        print(f"   Found {len(stations)} stations")
        
        # Export stations to CSV
        print("   Exporting to 'stations.csv'...")
        client.export_stations_to_csv(stations, "stations.csv")
        
        # Example 4: Get custom data items
        print("\n4. Getting custom data items...")
        custom_data_items = [
            "day-air-tmp-avg", "day-air-tmp-max", "day-air-tmp-min",
            "day-precip", "day-asce-eto"
        ]
        
        custom_data = client.get_data(
            targets=[2, 8],
            start_date=start_date,
            end_date=end_date,
            data_items=custom_data_items
        )
        
        print("   Exporting to 'custom_data.csv'...")
        client.export_to_csv(custom_data, "custom_data.csv")
        
        # Example 5: Get data and export in one step
        print("\n5. Getting data and exporting in one step...")
        combined_data = client.get_data_and_export_csv(
            targets=[2, 8, 127],
            start_date=start_date,
            end_date=end_date,
            filename="combined_weather_data.csv"
        )
        
        print("\n✅ All examples completed successfully!")
        print("\nGenerated files:")
        print("- station_weather_data.csv")
        print("- zip_weather_data.csv")
        print("- stations.csv")
        print("- custom_data.csv")
        print("- combined_weather_data.csv")
        
    except CimisAuthenticationError:
        print("❌ Authentication failed. Please check your API key.")
    except CimisAPIError as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
