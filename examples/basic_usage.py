#!/usr/bin/env python3
"""
Basic Usage Examples for Python CIMIS Client

This script demonstrates the fundamental features of the Python CIMIS Client library.
Replace 'your-api-key-here' with your actual CIMIS API key.

To get an API key:
1. Visit https://et.water.ca.gov/Rest/Index
2. Register for a free account
3. Generate your API key
"""

import os
from datetime import date, datetime, timedelta
from python_cimis import CimisClient


def main():
    # Initialize the client with your API key
    # Option 1: Direct string (not recommended for production)
    # client = CimisClient(app_key="your-api-key-here")
    
    # Option 2: Environment variable (recommended)
    api_key = os.getenv('CIMIS_API_KEY', 'your-api-key-here')
    client = CimisClient(app_key=api_key)
    
    print("🌤️  Python CIMIS Client - Basic Usage Examples")
    print("=" * 60)
    
    # Example 1: Get daily data for a specific station
    print("\n📊 Example 1: Daily Weather Data for Station 2 (Five Points)")
    print("-" * 50)
    
    try:
        # Get data for the last 7 days
        end_date = date.today() - timedelta(days=1)  # Yesterday
        start_date = end_date - timedelta(days=6)    # 7 days ago
        
        weather_data = client.get_daily_data(
            targets=[2],  # Station 2 (Five Points)
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"Retrieved data for {len(weather_data.get_all_records())} records")
        
        # Display first record as example
        if weather_data.providers:
            first_record = weather_data.providers[0].records[0] if weather_data.providers[0].records else None
            if first_record:
                print(f"Sample record for {first_record.date}:")
                print(f"  Station: {first_record.station}")
                print(f"  Available data items: {len(first_record.data_values)}")
                
                # Show some key weather values
                for key, value in list(first_record.data_values.items())[:3]:
                    print(f"  {key}: {value.value} {value.unit}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Get data by zip code
    print("\n🏠 Example 2: Weather Data by Zip Code")
    print("-" * 50)
    
    try:
        weather_data = client.get_daily_data(
            targets=["95823"],  # Sacramento area
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"Retrieved data for zip code 95823: {len(weather_data.get_all_records())} records")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Get station information
    print("\n🏛️  Example 3: Station Information")
    print("-" * 50)
    
    try:
        # Get all stations (limited to first 5 for display)
        stations = client.get_stations()
        print(f"Total stations available: {len(stations)}")
        
        # Display first 5 stations
        print("\nFirst 5 stations:")
        for station in stations[:5]:
            print(f"  Station {station.station_nbr}: {station.name} ({station.city})")
            print(f"    Active: {station.is_active}, ETo Station: {station.is_eto_station}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Export data to CSV
    print("\n💾 Example 4: Export Data to CSV")
    print("-" * 50)
    
    try:
        # Get recent data
        weather_data = client.get_daily_data(
            targets=[2, 8],  # Multiple stations
            start_date=start_date,
            end_date=end_date
        )
        
        # Export with automatic filename generation
        csv_file = client.export_to_csv(weather_data)
        print(f"Data exported to: {csv_file}")
        
        # Export with custom filename
        custom_csv = client.export_to_csv(
            weather_data, 
            filename="my_weather_data.csv"
        )
        print(f"Data also exported to: {custom_csv}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 5: Get data by coordinates
    print("\n🗺️  Example 5: Weather Data by Coordinates")
    print("-" * 50)
    
    try:
        # Sacramento coordinates
        weather_data = client.get_daily_data(
            targets=["lat=38.5816,lng=-121.4944"],
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"Retrieved data for Sacramento coordinates: {len(weather_data.get_all_records())} records")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 6: Hourly data
    print("\n⏰ Example 6: Hourly Weather Data")
    print("-" * 50)
    
    try:
        # Get hourly data for yesterday only (hourly data is large)
        yesterday = date.today() - timedelta(days=1)
        
        hourly_data = client.get_hourly_data(
            targets=[2],
            start_date=yesterday,
            end_date=yesterday
        )
        
        print(f"Retrieved hourly data: {len(hourly_data.get_all_records())} records")
        
        # Show hourly breakdown
        if hourly_data.providers and hourly_data.providers[0].records:
            hours_with_data = [r.hour for r in hourly_data.providers[0].records if r.hour]
            print(f"Hours with data: {len(hours_with_data)} hours")
            if hours_with_data:
                print(f"Sample hours: {hours_with_data[:5]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n✅ Examples completed!")
    print("\n💡 Tips:")
    print("- Set your API key as environment variable: CIMIS_API_KEY")
    print("- Use date objects for better type safety")
    print("- Check the generated CSV files for complete data")
    print("- Hourly data is only available from WSN stations")


if __name__ == "__main__":
    main()
