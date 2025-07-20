#!/usr/bin/env python3
"""
Example demonstrating the new csv=True parameter functionality
"""

from python_cimis.client import CimisClient

def example_csv_parameter():
    """Demonstrate the new csv=True parameter."""
    print("Example: Using csv=True parameter in get_daily_data() and get_hourly_data()")
    print("=" * 70)
    
    # Initialize client (replace with your actual API key)
    client = CimisClient(app_key="your-api-key-here")
    
    print("\n1. WITHOUT csv parameter (returns WeatherData object only):")
    print("   weather_data = client.get_daily_data(targets=[2], start_date='2023-01-01', end_date='2023-01-02')")
    print("   # Returns: WeatherData object")
    
    print("\n2. WITH csv=True parameter (returns tuple: WeatherData + CSV filename):")
    print("   weather_data, csv_file = client.get_daily_data(targets=[2], start_date='2023-01-01', end_date='2023-01-02', csv=True)")
    print("   # Returns: (WeatherData object, 'auto_generated_filename.csv')")
    
    print("\n3. WITH csv=True and custom filename:")
    print("   weather_data, csv_file = client.get_daily_data(targets=[2], start_date='2023-01-01', end_date='2023-01-02', csv=True, filename='my_data.csv')")
    print("   # Returns: (WeatherData object, 'my_data.csv')")
    
    print("\n4. Same functionality works for get_hourly_data() too:")
    print("   weather_data, csv_file = client.get_hourly_data(targets=[2], start_date='2023-01-01', end_date='2023-01-01', csv=True)")
    print("   # Returns: (WeatherData object, 'auto_generated_hourly_filename.csv')")
    
    print("\n✅ Enhancement Complete!")
    print("The csv=True parameter provides a convenient way to automatically export data to CSV")
    print("while still getting the WeatherData object for further processing.")

if __name__ == "__main__":
    example_csv_parameter()
