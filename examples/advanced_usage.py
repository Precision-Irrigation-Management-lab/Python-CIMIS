#!/usr/bin/env python3
"""
Advanced Usage Examples for Python CIMIS Client

This script demonstrates advanced features and patterns for using the Python CIMIS Client.
"""

import os
from datetime import date, datetime, timedelta
from pathlib import Path
from python_cimis import CimisClient
from python_cimis.exceptions import CimisAPIError, CimisConnectionError


def advanced_data_retrieval():
    """Demonstrate advanced data retrieval patterns."""
    print("🔬 Advanced Data Retrieval Examples")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    # Example 1: Multiple target types in one request
    print("\n1. Multiple Target Types")
    print("-" * 30)
    
    try:
        # Mix stations, zip codes, and coordinates
        mixed_targets = [
            "2",                              # Station number
            "95823",                          # Zip code
            "lat=38.5816,lng=-121.4944"      # Coordinates
        ]
        
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=3)
        
        weather_data = client.get_daily_data(
            targets=mixed_targets,
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"Total records from mixed targets: {len(weather_data.get_all_records())}")
        
        # Analyze by provider type
        for provider in weather_data.providers:
            print(f"  Provider: {provider.name} ({provider.type}) - {len(provider.records)} records")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Specific data items only
    print("\n2. Requesting Specific Data Items")
    print("-" * 30)
    
    try:
        # Only get temperature and ETo data
        specific_items = [
            "day-air-tmp-avg",
            "day-air-tmp-max", 
            "day-air-tmp-min",
            "day-eto"
        ]
        
        weather_data = client.get_daily_data(
            targets=[2],
            start_date=start_date,
            end_date=end_date,
            data_items=specific_items
        )
        
        print(f"Records with specific data items: {len(weather_data.get_all_records())}")
        
        # Show what data items we got
        if weather_data.providers and weather_data.providers[0].records:
            first_record = weather_data.providers[0].records[0]
            print(f"  Actual data items received: {list(first_record.data_values.keys())}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Explicit metric units (default is metric anyway)
    print("\n3. Using Explicit Metric Units")
    print("-" * 35)
    
    try:
        weather_data = client.get_daily_data(
            targets=[2],
            start_date=start_date,
            end_date=end_date,
            unit_of_measure='Metric'  # Explicit metric units (this is also the default)
        )
        
        if weather_data.providers and weather_data.providers[0].records:
            first_record = weather_data.providers[0].records[0]
            print(f"Sample metric data for {first_record.date}:")
            
            # Show temperature in Celsius
            temp_data = first_record.data_values.get('day-air-tmp-avg')
            if temp_data:
                print(f"  Average Temperature: {temp_data.value} {temp_data.unit}")
        
    except Exception as e:
        print(f"Error: {e}")


def data_analysis_examples():
    """Demonstrate data analysis patterns."""
    print("\n📈 Data Analysis Examples")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Get a month of data for analysis
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=30)
        
        weather_data = client.get_daily_data(
            targets=[2],  # Five Points station
            start_date=start_date,
            end_date=end_date
        )
        
        all_records = weather_data.get_all_records()
        print(f"Analyzing {len(all_records)} days of data")
        
        # Temperature analysis
        temperatures = []
        eto_values = []
        
        for record in all_records:
            temp_avg = record.data_values.get('day-air-tmp-avg')
            eto = record.data_values.get('day-eto')
            
            if temp_avg and temp_avg.value:
                try:
                    temperatures.append(float(temp_avg.value))
                except ValueError:
                    pass
            
            if eto and eto.value:
                try:
                    eto_values.append(float(eto.value))
                except ValueError:
                    pass
        
        if temperatures:
            print(f"\nTemperature Analysis (°F):")
            print(f"  Average: {sum(temperatures)/len(temperatures):.1f}°F")
            print(f"  Maximum: {max(temperatures):.1f}°F")
            print(f"  Minimum: {min(temperatures):.1f}°F")
        
        if eto_values:
            print(f"\nET₀ Analysis (inches):")
            print(f"  Average daily: {sum(eto_values)/len(eto_values):.3f} in")
            print(f"  Total period: {sum(eto_values):.2f} in")
            print(f"  Maximum daily: {max(eto_values):.3f} in")
        
        # Find days with missing data
        missing_data_days = []
        for record in all_records:
            if not record.data_values:
                missing_data_days.append(record.date)
        
        if missing_data_days:
            print(f"\nDays with missing data: {len(missing_data_days)}")
            print(f"  Examples: {missing_data_days[:3]}")
        else:
            print(f"\n✅ No missing data days found!")
    
    except Exception as e:
        print(f"Error: {e}")


def csv_export_patterns():
    """Demonstrate various CSV export patterns."""
    print("\n💾 CSV Export Patterns")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Get some sample data
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
        
        weather_data = client.get_daily_data(
            targets=[2, 8],  # Multiple stations
            start_date=start_date,
            end_date=end_date
        )
        
        # Create exports directory
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        
        # Pattern 1: Auto-generated filename
        auto_filename = client.export_to_csv(weather_data)
        print(f"1. Auto-generated filename: {Path(auto_filename).name}")
        
        # Pattern 2: Custom filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        custom_file = exports_dir / f"weather_data_{timestamp}.csv"
        client.export_to_csv(weather_data, filename=custom_file)
        print(f"2. Timestamped filename: {custom_file.name}")
        
        # Pattern 3: Organized by date range
        date_str = f"{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}"
        date_file = exports_dir / f"weather_{date_str}.csv"
        client.export_to_csv(weather_data, filename=date_file)
        print(f"3. Date-organized filename: {date_file.name}")
        
        # Pattern 4: Station-specific exports
        for provider in weather_data.providers:
            if provider.records and provider.records[0].station:
                station_num = provider.records[0].station
                station_file = exports_dir / f"station_{station_num}_{date_str}.csv"
                
                # Create weather data with just this provider
                single_provider_data = weather_data.__class__()
                single_provider_data.providers = [provider]
                
                client.export_to_csv(single_provider_data, filename=station_file)
                print(f"4. Station-specific file: {station_file.name}")
        
        # Get and export station information
        stations = client.get_stations()
        stations_file = client.export_stations_to_csv(stations[:10])  # First 10 stations
        print(f"5. Stations info export: {Path(stations_file).name}")
        
    except Exception as e:
        print(f"Error: {e}")


def error_handling_examples():
    """Demonstrate proper error handling."""
    print("\n⚠️  Error Handling Examples")
    print("=" * 50)
    
    # Example with invalid API key
    print("\n1. Invalid API Key Handling")
    print("-" * 30)
    
    try:
        invalid_client = CimisClient(app_key="invalid-key")
        invalid_client.get_daily_data(
            targets=[2],
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() - timedelta(days=1)
        )
    except CimisAPIError as e:
        print(f"✅ Caught API error: {e}")
        print(f"   Error code: {e.error_code}")
        print(f"   HTTP code: {e.http_code}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Example with invalid station
    print("\n2. Invalid Station Handling")
    print("-" * 30)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        weather_data = client.get_daily_data(
            targets=[99999],  # Non-existent station
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() - timedelta(days=1)
        )
        
        # Check if we got any data
        if not weather_data.get_all_records():
            print("✅ No data returned for invalid station (graceful handling)")
        
    except CimisAPIError as e:
        print(f"✅ API error for invalid station: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Example with connection timeout
    print("\n3. Timeout Handling")
    print("-" * 30)
    
    try:
        timeout_client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'), timeout=0.001)
        timeout_client.get_daily_data(
            targets=[2],
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() - timedelta(days=1)
        )
    except CimisConnectionError as e:
        print(f"✅ Caught connection error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def filtering_and_processing():
    """Demonstrate data filtering and processing."""
    print("\n🔍 Data Filtering and Processing")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Get data from multiple stations
        weather_data = client.get_daily_data(
            targets=[2, 8, 12],  # Multiple stations
            start_date=date.today() - timedelta(days=14),
            end_date=date.today() - timedelta(days=1)
        )
        
        print(f"Total records retrieved: {len(weather_data.get_all_records())}")
        
        # Filter by station
        station_2_data = weather_data.get_records_by_station("2")
        print(f"Station 2 records: {len(station_2_data)}")
        
        # Filter by date range
        recent_date = date.today() - timedelta(days=7)
        recent_records = weather_data.get_records_by_date_range(
            start_date=recent_date,
            end_date=date.today() - timedelta(days=1)
        )
        print(f"Recent week records: {len(recent_records)}")
        
        # Filter by provider type
        station_providers = [p for p in weather_data.providers if p.type == "station"]
        spatial_providers = [p for p in weather_data.providers if p.type == "spatial"]
        
        print(f"Station providers: {len(station_providers)}")
        print(f"Spatial providers: {len(spatial_providers)}")
        
        # Process temperature data
        temp_data = []
        for record in weather_data.get_all_records():
            temp_avg = record.data_values.get('day-air-tmp-avg')
            if temp_avg and temp_avg.value:
                try:
                    temp_data.append({
                        'date': record.date,
                        'station': record.station,
                        'temperature': float(temp_avg.value),
                        'unit': temp_avg.unit
                    })
                except ValueError:
                    pass
        
        if temp_data:
            print(f"\nProcessed temperature data: {len(temp_data)} points")
            # Find hottest day
            hottest = max(temp_data, key=lambda x: x['temperature'])
            print(f"Hottest day: {hottest['date']} at Station {hottest['station']} - {hottest['temperature']}°F")
    
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all advanced examples."""
    print("🚀 Python CIMIS Client - Advanced Usage Examples")
    print("=" * 60)
    
    advanced_data_retrieval()
    data_analysis_examples()
    csv_export_patterns()
    error_handling_examples()
    filtering_and_processing()
    
    print("\n✅ All advanced examples completed!")
    print("\n💡 Advanced Tips:")
    print("- Always handle exceptions appropriately")
    print("- Use specific data items to reduce response size")
    print("- Implement retry logic for production applications")
    print("- Consider caching results for repeated requests")
    print("- Check data quality flags (QC codes) for important analyses")


if __name__ == "__main__":
    main()
