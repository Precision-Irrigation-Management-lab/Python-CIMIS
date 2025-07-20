#!/usr/bin/env python3
"""
Real-World Use Cases for Python CIMIS Client

This script demonstrates practical real-world applications of the CIMIS API
for agriculture, irrigation management, and climate analysis.
"""

import os
from datetime import date, datetime, timedelta
from pathlib import Path
from python_cimis import CimisClient


def irrigation_scheduling_example():
    """Example: Calculate irrigation needs based on ETo data."""
    print("💧 Irrigation Scheduling Use Case")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Get last week's data for a farm location
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
        
        # Use coordinates for a specific field location
        farm_location = "lat=36.3360,lng=-120.1130"  # Five Points area
        
        weather_data = client.get_daily_data(
            targets=[farm_location],
            start_date=start_date,
            end_date=end_date,
            data_items=["day-eto", "day-precip"]  # Only need ETo and precipitation
        )
        
        records = weather_data.get_all_records()
        print(f"Analyzing {len(records)} days of irrigation data")
        
        # Calculate irrigation needs
        total_eto = 0
        total_precip = 0
        irrigation_days = []
        
        for record in records:
            eto_data = record.data_values.get('day-eto')
            precip_data = record.data_values.get('day-precip')
            
            daily_eto = 0
            daily_precip = 0
            
            if eto_data and eto_data.value:
                try:
                    daily_eto = float(eto_data.value)
                    total_eto += daily_eto
                except ValueError:
                    pass
            
            if precip_data and precip_data.value:
                try:
                    daily_precip = float(precip_data.value)
                    total_precip += daily_precip
                except ValueError:
                    pass
            
            # Irrigation needed if ETo > precipitation + 0.1" buffer
            net_water_need = daily_eto - daily_precip
            if net_water_need > 0.1:
                irrigation_days.append({
                    'date': record.date,
                    'eto': daily_eto,
                    'precip': daily_precip,
                    'need': net_water_need
                })
        
        print(f"\nIrrigation Analysis:")
        print(f"  Total ETo for period: {total_eto:.2f} inches")
        print(f"  Total precipitation: {total_precip:.2f} inches")
        print(f"  Net irrigation need: {total_eto - total_precip:.2f} inches")
        print(f"  Days requiring irrigation: {len(irrigation_days)}")
        
        if irrigation_days:
            print(f"\nIrrigation Schedule:")
            for day in irrigation_days:
                print(f"  {day['date']}: Apply {day['need']:.2f}\" (ETo: {day['eto']:.2f}\", Rain: {day['precip']:.2f}\")")
    
    except Exception as e:
        print(f"Error: {e}")


def crop_water_use_analysis():
    """Example: Analyze crop water use for different growth stages."""
    print("\n🌱 Crop Water Use Analysis")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Analyze growing season data (April through September)
        current_year = date.today().year
        growing_season_start = date(current_year, 4, 1)
        growing_season_end = date(current_year, 9, 30)
        
        # If current date is before growing season, use previous year
        if date.today() < growing_season_start:
            growing_season_start = date(current_year - 1, 4, 1)
            growing_season_end = date(current_year - 1, 9, 30)
        
        print(f"Analyzing growing season: {growing_season_start} to {growing_season_end}")
        
        # Get data for multiple agricultural regions
        ag_stations = [2, 8, 12, 15]  # Various Central Valley stations
        
        weather_data = client.get_daily_data(
            targets=ag_stations,
            start_date=growing_season_start,
            end_date=min(growing_season_end, date.today() - timedelta(days=1)),
            data_items=["day-eto", "day-air-tmp-avg", "day-air-tmp-max", "day-precip"]
        )
        
        # Analyze by station
        for station in ag_stations:
            station_records = weather_data.get_records_by_station(str(station))
            
            if not station_records:
                continue
            
            station_name = f"Station {station}"
            total_eto = 0
            total_precip = 0
            avg_temps = []
            hot_days = 0  # Days over 95°F
            
            for record in station_records:
                # ETo accumulation
                eto_data = record.data_values.get('day-eto')
                if eto_data and eto_data.value:
                    try:
                        total_eto += float(eto_data.value)
                    except ValueError:
                        pass
                
                # Precipitation accumulation
                precip_data = record.data_values.get('day-precip')
                if precip_data and precip_data.value:
                    try:
                        total_precip += float(precip_data.value)
                    except ValueError:
                        pass
                
                # Temperature analysis
                temp_avg = record.data_values.get('day-air-tmp-avg')
                temp_max = record.data_values.get('day-air-tmp-max')
                
                if temp_avg and temp_avg.value:
                    try:
                        avg_temps.append(float(temp_avg.value))
                    except ValueError:
                        pass
                
                if temp_max and temp_max.value:
                    try:
                        if float(temp_max.value) > 95:
                            hot_days += 1
                    except ValueError:
                        pass
            
            print(f"\n{station_name} Analysis:")
            print(f"  Total ETo: {total_eto:.1f} inches")
            print(f"  Total precipitation: {total_precip:.1f} inches")
            print(f"  Net water need: {total_eto - total_precip:.1f} inches")
            if avg_temps:
                print(f"  Average temperature: {sum(avg_temps)/len(avg_temps):.1f}°F")
            print(f"  Hot days (>95°F): {hot_days}")
            
            # Crop coefficient estimates (example for tomatoes)
            crop_et = total_eto * 1.15  # Kc = 1.15 for mature tomatoes
            print(f"  Estimated tomato water use: {crop_et:.1f} inches")
    
    except Exception as e:
        print(f"Error: {e}")


def weather_monitoring_dashboard():
    """Example: Create a weather monitoring summary for multiple locations."""
    print("\n📊 Weather Monitoring Dashboard")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Define monitoring locations with names
        locations = {
            "2": "Five Points",
            "8": "Tulare", 
            "12": "Modesto",
            "15": "Fresno",
            "95823": "Sacramento (Zip)"
        }
        
        # Get recent data
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
        
        weather_data = client.get_daily_data(
            targets=list(locations.keys()),
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"Weather Summary for {start_date} to {end_date}")
        print("-" * 60)
        
        # Create summary for each location
        for target_id, location_name in locations.items():
            records = weather_data.get_records_by_station(target_id)
            
            if not records:
                print(f"\n{location_name}: No data available")
                continue
            
            # Calculate averages and totals
            temperatures = []
            eto_values = []
            precip_values = []
            
            for record in records:
                temp_data = record.data_values.get('day-air-tmp-avg')
                eto_data = record.data_values.get('day-eto')
                precip_data = record.data_values.get('day-precip')
                
                if temp_data and temp_data.value:
                    try:
                        temperatures.append(float(temp_data.value))
                    except ValueError:
                        pass
                
                if eto_data and eto_data.value:
                    try:
                        eto_values.append(float(eto_data.value))
                    except ValueError:
                        pass
                
                if precip_data and precip_data.value:
                    try:
                        precip_values.append(float(precip_data.value))
                    except ValueError:
                        pass
            
            print(f"\n📍 {location_name} (ID: {target_id})")
            print(f"   Records: {len(records)} days")
            
            if temperatures:
                print(f"   Avg Temp: {sum(temperatures)/len(temperatures):.1f}°F")
                print(f"   Max Temp: {max(temperatures):.1f}°F")
                print(f"   Min Temp: {min(temperatures):.1f}°F")
            
            if eto_values:
                print(f"   Total ETo: {sum(eto_values):.2f} inches")
                print(f"   Avg Daily ETo: {sum(eto_values)/len(eto_values):.3f} inches")
            
            if precip_values:
                total_precip = sum(precip_values)
                print(f"   Total Precipitation: {total_precip:.2f} inches")
                if total_precip > 0:
                    rainy_days = len([p for p in precip_values if p > 0.01])
                    print(f"   Rainy Days: {rainy_days}")
            
            # Calculate water balance
            if eto_values and precip_values:
                water_deficit = sum(eto_values) - sum(precip_values)
                if water_deficit > 0:
                    print(f"   💧 Irrigation Need: {water_deficit:.2f} inches")
                else:
                    print(f"   💧 Water Surplus: {abs(water_deficit):.2f} inches")
        
        # Export dashboard data
        dashboard_file = client.export_to_csv(
            weather_data,
            filename=f"weather_dashboard_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
        )
        print(f"\n💾 Dashboard data exported to: {Path(dashboard_file).name}")
    
    except Exception as e:
        print(f"Error: {e}")


def frost_protection_alert():
    """Example: Frost protection monitoring for sensitive crops."""
    print("\n🧊 Frost Protection Alert System")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Monitor frost-sensitive crop areas
        frost_sensitive_locations = [
            "2",   # Five Points - stone fruits
            "8",   # Tulare - citrus
            "12",  # Modesto - almonds
        ]
        
        location_names = {
            "2": "Five Points (Stone Fruits)",
            "8": "Tulare (Citrus)",
            "12": "Modesto (Almonds)"
        }
        
        # Get recent temperature data
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
        
        weather_data = client.get_daily_data(
            targets=frost_sensitive_locations,
            start_date=start_date,
            end_date=end_date,
            data_items=["day-air-tmp-min", "day-air-tmp-avg", "day-air-tmp-max"]
        )
        
        print("Frost Risk Assessment:")
        print("-" * 30)
        
        # Frost thresholds (in Fahrenheit)
        frost_thresholds = {
            "2": 28,   # Stone fruits - critical at 28°F
            "8": 32,   # Citrus - damage at 32°F
            "12": 26   # Almonds - critical at 26°F during bloom
        }
        
        for station_id in frost_sensitive_locations:
            records = weather_data.get_records_by_station(station_id)
            location_name = location_names.get(station_id, f"Station {station_id}")
            threshold = frost_thresholds.get(station_id, 32)
            
            if not records:
                continue
            
            print(f"\n🌡️  {location_name}")
            print(f"   Frost threshold: {threshold}°F")
            
            frost_events = []
            near_frost_events = []
            
            for record in records:
                min_temp_data = record.data_values.get('day-air-tmp-min')
                
                if min_temp_data and min_temp_data.value:
                    try:
                        min_temp = float(min_temp_data.value)
                        
                        if min_temp <= threshold:
                            frost_events.append({
                                'date': record.date,
                                'min_temp': min_temp,
                                'severity': 'CRITICAL' if min_temp <= threshold - 4 else 'MODERATE'
                            })
                        elif min_temp <= threshold + 5:
                            near_frost_events.append({
                                'date': record.date,
                                'min_temp': min_temp
                            })
                    except ValueError:
                        pass
            
            if frost_events:
                print(f"   🚨 FROST EVENTS: {len(frost_events)}")
                for event in frost_events:
                    print(f"      {event['date']}: {event['min_temp']:.1f}°F ({event['severity']})")
            elif near_frost_events:
                print(f"   ⚠️  Near-frost conditions: {len(near_frost_events)} days")
                for event in near_frost_events[:3]:  # Show first 3
                    print(f"      {event['date']}: {event['min_temp']:.1f}°F")
            else:
                print(f"   ✅ No frost risk detected")
            
            # Calculate frost-free days
            all_min_temps = []
            for record in records:
                min_temp_data = record.data_values.get('day-air-tmp-min')
                if min_temp_data and min_temp_data.value:
                    try:
                        all_min_temps.append(float(min_temp_data.value))
                    except ValueError:
                        pass
            
            if all_min_temps:
                avg_min = sum(all_min_temps) / len(all_min_temps)
                print(f"   Average minimum temp: {avg_min:.1f}°F")
    
    except Exception as e:
        print(f"Error: {e}")


def climate_trend_analysis():
    """Example: Long-term climate trend analysis."""
    print("\n📈 Climate Trend Analysis")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Compare same period across multiple years
        current_year = date.today().year
        analysis_period_days = 30
        
        # Use a consistent date range (e.g., July 1-30) for comparison
        base_month = 7
        base_day = 1
        
        years_to_compare = [current_year - 2, current_year - 1]
        station_id = "2"  # Five Points for consistency
        
        print(f"Comparing {base_month}/{base_day} to {base_month}/{base_day + analysis_period_days - 1} across years")
        
        yearly_data = {}
        
        for year in years_to_compare:
            start_date = date(year, base_month, base_day)
            end_date = start_date + timedelta(days=analysis_period_days - 1)
            
            # Skip if end_date is in the future
            if end_date > date.today():
                continue
            
            try:
                weather_data = client.get_daily_data(
                    targets=[station_id],
                    start_date=start_date,
                    end_date=end_date,
                    data_items=["day-air-tmp-avg", "day-air-tmp-max", "day-eto", "day-precip"]
                )
                
                records = weather_data.get_records_by_station(station_id)
                
                if records:
                    yearly_data[year] = {
                        'temperatures': [],
                        'max_temps': [],
                        'eto_values': [],
                        'precip_values': []
                    }
                    
                    for record in records:
                        temp_avg = record.data_values.get('day-air-tmp-avg')
                        temp_max = record.data_values.get('day-air-tmp-max')
                        eto = record.data_values.get('day-eto')
                        precip = record.data_values.get('day-precip')
                        
                        if temp_avg and temp_avg.value:
                            try:
                                yearly_data[year]['temperatures'].append(float(temp_avg.value))
                            except ValueError:
                                pass
                        
                        if temp_max and temp_max.value:
                            try:
                                yearly_data[year]['max_temps'].append(float(temp_max.value))
                            except ValueError:
                                pass
                        
                        if eto and eto.value:
                            try:
                                yearly_data[year]['eto_values'].append(float(eto.value))
                            except ValueError:
                                pass
                        
                        if precip and precip.value:
                            try:
                                yearly_data[year]['precip_values'].append(float(precip.value))
                            except ValueError:
                                pass
            
            except Exception as e:
                print(f"Could not get data for {year}: {e}")
        
        # Compare years
        print(f"\nClimate Comparison for Station {station_id}:")
        print("-" * 40)
        
        for year, data in yearly_data.items():
            print(f"\n📅 Year {year}:")
            
            if data['temperatures']:
                avg_temp = sum(data['temperatures']) / len(data['temperatures'])
                print(f"   Average Temperature: {avg_temp:.1f}°F")
            
            if data['max_temps']:
                avg_max = sum(data['max_temps']) / len(data['max_temps'])
                extreme_days = len([t for t in data['max_temps'] if t > 100])
                print(f"   Average Max Temp: {avg_max:.1f}°F")
                print(f"   Days over 100°F: {extreme_days}")
            
            if data['eto_values']:
                total_eto = sum(data['eto_values'])
                print(f"   Total ETo: {total_eto:.2f} inches")
            
            if data['precip_values']:
                total_precip = sum(data['precip_values'])
                print(f"   Total Precipitation: {total_precip:.2f} inches")
        
        # Calculate trends if we have multiple years
        if len(yearly_data) >= 2:
            years = sorted(yearly_data.keys())
            print(f"\n📊 Trends from {years[0]} to {years[-1]}:")
            
            for metric in ['temperatures', 'eto_values', 'precip_values']:
                values_by_year = []
                for year in years:
                    if yearly_data[year][metric]:
                        if metric == 'temperatures':
                            values_by_year.append(sum(yearly_data[year][metric]) / len(yearly_data[year][metric]))
                        else:
                            values_by_year.append(sum(yearly_data[year][metric]))
                
                if len(values_by_year) >= 2:
                    change = values_by_year[-1] - values_by_year[0]
                    metric_name = metric.replace('_', ' ').title()
                    print(f"   {metric_name}: {change:+.2f} {'°F' if 'temp' in metric else 'inches'}")
    
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all real-world use case examples."""
    print("🌾 Python CIMIS Client - Real-World Use Cases")
    print("=" * 60)
    
    irrigation_scheduling_example()
    crop_water_use_analysis()
    weather_monitoring_dashboard()
    frost_protection_alert()
    climate_trend_analysis()
    
    print("\n✅ All real-world examples completed!")
    print("\n🎯 Implementation Tips:")
    print("- Set up automated daily runs for irrigation scheduling")
    print("- Use webhook notifications for frost alerts")
    print("- Store historical data in a database for trend analysis")
    print("- Combine with crop coefficients for precise water management")
    print("- Integrate with soil moisture sensors for complete irrigation control")


if __name__ == "__main__":
    main()
