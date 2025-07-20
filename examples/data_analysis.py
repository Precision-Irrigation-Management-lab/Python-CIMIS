#!/usr/bin/env python3
"""
Data Analysis Examples for Python CIMIS Client

This script demonstrates how to perform various data analysis tasks
using weather data from the CIMIS API.
"""

import os
from datetime import date, datetime, timedelta
from pathlib import Path
from python_cimis import CimisClient


def statistical_analysis():
    """Demonstrate statistical analysis of weather data."""
    print("📊 Statistical Analysis Examples")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Get a month of data for statistical analysis
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=30)
        
        weather_data = client.get_daily_data(
            targets=[2],  # Five Points station
            start_date=start_date,
            end_date=end_date
        )
        
        records = weather_data.get_all_records()
        print(f"Analyzing {len(records)} days of data")
        
        # Extract temperature data
        temperatures = []
        eto_values = []
        humidity_values = []
        
        for record in records:
            temp_data = record.data_values.get('day-air-tmp-avg')
            eto_data = record.data_values.get('day-eto')
            humidity_data = record.data_values.get('day-rel-hum-avg')
            
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
            
            if humidity_data and humidity_data.value:
                try:
                    humidity_values.append(float(humidity_data.value))
                except ValueError:
                    pass
        
        # Temperature statistics
        if temperatures:
            temps_sorted = sorted(temperatures)
            n = len(temps_sorted)
            
            mean_temp = sum(temperatures) / n
            median_temp = temps_sorted[n//2] if n % 2 == 1 else (temps_sorted[n//2-1] + temps_sorted[n//2]) / 2
            
            # Calculate standard deviation
            variance = sum((t - mean_temp) ** 2 for t in temperatures) / n
            std_dev = variance ** 0.5
            
            print(f"\n🌡️  Temperature Statistics:")
            print(f"   Mean: {mean_temp:.1f}°F")
            print(f"   Median: {median_temp:.1f}°F")
            print(f"   Standard Deviation: {std_dev:.1f}°F")
            print(f"   Range: {min(temperatures):.1f}°F to {max(temperatures):.1f}°F")
            
            # Percentiles
            p25 = temps_sorted[n//4]
            p75 = temps_sorted[3*n//4]
            print(f"   25th Percentile: {p25:.1f}°F")
            print(f"   75th Percentile: {p75:.1f}°F")
            
            # Temperature distribution
            cool_days = len([t for t in temperatures if t < 70])
            mild_days = len([t for t in temperatures if 70 <= t < 85])
            hot_days = len([t for t in temperatures if t >= 85])
            
            print(f"\n   Temperature Distribution:")
            print(f"   Cool days (<70°F): {cool_days} ({cool_days/n*100:.1f}%)")
            print(f"   Mild days (70-85°F): {mild_days} ({mild_days/n*100:.1f}%)")
            print(f"   Hot days (≥85°F): {hot_days} ({hot_days/n*100:.1f}%)")
        
        # ETo statistics
        if eto_values:
            mean_eto = sum(eto_values) / len(eto_values)
            total_eto = sum(eto_values)
            
            print(f"\n💧 Evapotranspiration Statistics:")
            print(f"   Mean daily ETo: {mean_eto:.3f} inches")
            print(f"   Total period ETo: {total_eto:.2f} inches")
            print(f"   Max daily ETo: {max(eto_values):.3f} inches")
            print(f"   Min daily ETo: {min(eto_values):.3f} inches")
            
            # ETo efficiency classes
            low_eto = len([e for e in eto_values if e < 0.15])
            med_eto = len([e for e in eto_values if 0.15 <= e < 0.25])
            high_eto = len([e for e in eto_values if e >= 0.25])
            
            print(f"\n   ETo Distribution:")
            print(f"   Low ETo days (<0.15\"): {low_eto}")
            print(f"   Medium ETo days (0.15-0.25\"): {med_eto}")
            print(f"   High ETo days (≥0.25\"): {high_eto}")
        
        # Correlation analysis (simple)
        if len(temperatures) == len(eto_values) and len(temperatures) > 1:
            # Calculate correlation between temperature and ETo
            temp_mean = sum(temperatures) / len(temperatures)
            eto_mean = sum(eto_values) / len(eto_values)
            
            numerator = sum((temperatures[i] - temp_mean) * (eto_values[i] - eto_mean) 
                          for i in range(len(temperatures)))
            temp_var = sum((t - temp_mean) ** 2 for t in temperatures)
            eto_var = sum((e - eto_mean) ** 2 for e in eto_values)
            
            if temp_var > 0 and eto_var > 0:
                correlation = numerator / (temp_var * eto_var) ** 0.5
                print(f"\n🔗 Correlation Analysis:")
                print(f"   Temperature vs ETo correlation: {correlation:.3f}")
                
                if correlation > 0.7:
                    print("   Strong positive correlation")
                elif correlation > 0.3:
                    print("   Moderate positive correlation")
                else:
                    print("   Weak correlation")
    
    except Exception as e:
        print(f"Error: {e}")


def time_series_analysis():
    """Demonstrate time series analysis patterns."""
    print("\n📈 Time Series Analysis")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Get longer time series for trend analysis
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=90)  # 3 months
        
        weather_data = client.get_daily_data(
            targets=[2],
            start_date=start_date,
            end_date=end_date,
            data_items=["day-air-tmp-avg", "day-eto"]
        )
        
        records = weather_data.get_all_records()
        print(f"Analyzing {len(records)} days time series")
        
        # Create time series data
        time_series = []
        for record in records:
            temp_data = record.data_values.get('day-air-tmp-avg')
            eto_data = record.data_values.get('day-eto')
            
            if temp_data and temp_data.value and eto_data and eto_data.value:
                try:
                    time_series.append({
                        'date': record.date,
                        'temperature': float(temp_data.value),
                        'eto': float(eto_data.value)
                    })
                except ValueError:
                    pass
        
        if len(time_series) < 30:
            print("Insufficient data for time series analysis")
            return
        
        # Calculate moving averages
        def moving_average(data, window):
            """Calculate moving average with given window size."""
            if len(data) < window:
                return data
            
            result = []
            for i in range(len(data)):
                if i < window - 1:
                    result.append(data[i])
                else:
                    avg = sum(data[i-window+1:i+1]) / window
                    result.append(avg)
            return result
        
        temperatures = [d['temperature'] for d in time_series]
        eto_values = [d['eto'] for d in time_series]
        
        # 7-day moving averages
        temp_ma7 = moving_average(temperatures, 7)
        eto_ma7 = moving_average(eto_values, 7)
        
        print(f"\n📊 Moving Average Analysis:")
        print(f"   Current 7-day temp average: {temp_ma7[-1]:.1f}°F")
        print(f"   Previous 7-day temp average: {temp_ma7[-8]:.1f}°F")
        temp_trend = temp_ma7[-1] - temp_ma7[-8]
        print(f"   Temperature trend: {temp_trend:+.1f}°F per week")
        
        print(f"   Current 7-day ETo average: {eto_ma7[-1]:.3f} inches")
        print(f"   Previous 7-day ETo average: {eto_ma7[-8]:.3f} inches")
        eto_trend = eto_ma7[-1] - eto_ma7[-8]
        print(f"   ETo trend: {eto_trend:+.3f} inches per week")
        
        # Detect patterns
        recent_temps = temperatures[-14:]  # Last 2 weeks
        if len(recent_temps) >= 14:
            first_week = recent_temps[:7]
            second_week = recent_temps[7:]
            
            avg_first = sum(first_week) / 7
            avg_second = sum(second_week) / 7
            
            print(f"\n🔍 Pattern Detection:")
            print(f"   Week 1 average: {avg_first:.1f}°F")
            print(f"   Week 2 average: {avg_second:.1f}°F")
            
            if avg_second > avg_first + 3:
                print("   📈 Warming trend detected")
            elif avg_second < avg_first - 3:
                print("   📉 Cooling trend detected")
            else:
                print("   ➡️  Stable temperature pattern")
        
        # Volatility analysis
        temp_changes = [abs(temperatures[i] - temperatures[i-1]) 
                       for i in range(1, len(temperatures))]
        avg_volatility = sum(temp_changes) / len(temp_changes)
        
        print(f"\n🌡️  Temperature Volatility:")
        print(f"   Average daily change: {avg_volatility:.1f}°F")
        
        large_changes = [c for c in temp_changes if c > 10]
        print(f"   Days with >10°F change: {len(large_changes)}")
        
        if large_changes:
            print(f"   Largest daily change: {max(large_changes):.1f}°F")
    
    except Exception as e:
        print(f"Error: {e}")


def comparative_analysis():
    """Compare weather patterns across multiple locations."""
    print("\n🗺️  Comparative Location Analysis")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Compare different climate zones
        locations = {
            "2": "Five Points (Central Valley)",
            "8": "Tulare (San Joaquin Valley)",
            "12": "Modesto (Northern Central Valley)",
            "15": "Fresno (Southern Central Valley)"
        }
        
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=30)
        
        weather_data = client.get_daily_data(
            targets=list(locations.keys()),
            start_date=start_date,
            end_date=end_date,
            data_items=["day-air-tmp-avg", "day-air-tmp-max", "day-air-tmp-min", "day-eto", "day-precip"]
        )
        
        location_stats = {}
        
        for station_id, location_name in locations.items():
            records = weather_data.get_records_by_station(station_id)
            
            if not records:
                continue
            
            temps_avg = []
            temps_max = []
            temps_min = []
            eto_vals = []
            precip_vals = []
            
            for record in records:
                temp_avg = record.data_values.get('day-air-tmp-avg')
                temp_max = record.data_values.get('day-air-tmp-max')
                temp_min = record.data_values.get('day-air-tmp-min')
                eto = record.data_values.get('day-eto')
                precip = record.data_values.get('day-precip')
                
                if temp_avg and temp_avg.value:
                    try:
                        temps_avg.append(float(temp_avg.value))
                    except ValueError:
                        pass
                
                if temp_max and temp_max.value:
                    try:
                        temps_max.append(float(temp_max.value))
                    except ValueError:
                        pass
                
                if temp_min and temp_min.value:
                    try:
                        temps_min.append(float(temp_min.value))
                    except ValueError:
                        pass
                
                if eto and eto.value:
                    try:
                        eto_vals.append(float(eto.value))
                    except ValueError:
                        pass
                
                if precip and precip.value:
                    try:
                        precip_vals.append(float(precip.value))
                    except ValueError:
                        pass
            
            location_stats[station_id] = {
                'name': location_name,
                'avg_temp': sum(temps_avg) / len(temps_avg) if temps_avg else 0,
                'max_temp': max(temps_max) if temps_max else 0,
                'min_temp': min(temps_min) if temps_min else 0,
                'total_eto': sum(eto_vals) if eto_vals else 0,
                'total_precip': sum(precip_vals) if precip_vals else 0,
                'temp_range': (max(temps_max) - min(temps_min)) if temps_max and temps_min else 0,
                'days': len(records)
            }
        
        # Display comparison
        print(f"Climate Comparison ({start_date} to {end_date}):")
        print("-" * 60)
        
        for station_id, stats in location_stats.items():
            print(f"\n📍 {stats['name']}")
            print(f"   Data days: {stats['days']}")
            print(f"   Average temperature: {stats['avg_temp']:.1f}°F")
            print(f"   Temperature range: {stats['temp_range']:.1f}°F")
            print(f"   Total ETo: {stats['total_eto']:.2f} inches")
            print(f"   Total precipitation: {stats['total_precip']:.2f} inches")
            
            water_balance = stats['total_eto'] - stats['total_precip']
            print(f"   Water deficit: {water_balance:.2f} inches")
        
        # Find extremes
        if location_stats:
            hottest_location = max(location_stats.items(), key=lambda x: x[1]['avg_temp'])
            coolest_location = min(location_stats.items(), key=lambda x: x[1]['avg_temp'])
            driest_location = max(location_stats.items(), key=lambda x: x[1]['total_eto'] - x[1]['total_precip'])
            
            print(f"\n🏆 Regional Extremes:")
            print(f"   Hottest: {hottest_location[1]['name']} ({hottest_location[1]['avg_temp']:.1f}°F avg)")
            print(f"   Coolest: {coolest_location[1]['name']} ({coolest_location[1]['avg_temp']:.1f}°F avg)")
            print(f"   Driest: {driest_location[1]['name']} ({driest_location[1]['total_eto'] - driest_location[1]['total_precip']:.2f}\" deficit)")
    
    except Exception as e:
        print(f"Error: {e}")


def growing_degree_days():
    """Calculate Growing Degree Days (GDD) for crop development."""
    print("\n🌱 Growing Degree Days Analysis")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        # Get temperature data for GDD calculation
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=60)  # 2 months
        
        weather_data = client.get_daily_data(
            targets=[2],  # Five Points
            start_date=start_date,
            end_date=end_date,
            data_items=["day-air-tmp-max", "day-air-tmp-min"]
        )
        
        records = weather_data.get_all_records()
        print(f"Calculating GDD for {len(records)} days")
        
        # GDD calculation for different crops
        crop_base_temps = {
            'Corn': 50,
            'Tomatoes': 50,
            'Almonds': 55,
            'Grapes': 50,
            'Cotton': 60
        }
        
        daily_gdd = {}
        cumulative_gdd = {}
        
        # Initialize
        for crop in crop_base_temps:
            daily_gdd[crop] = []
            cumulative_gdd[crop] = 0
        
        for record in records:
            temp_max_data = record.data_values.get('day-air-tmp-max')
            temp_min_data = record.data_values.get('day-air-tmp-min')
            
            if temp_max_data and temp_max_data.value and temp_min_data and temp_min_data.value:
                try:
                    temp_max = float(temp_max_data.value)
                    temp_min = float(temp_min_data.value)
                    
                    # Calculate daily average temperature
                    daily_avg = (temp_max + temp_min) / 2
                    
                    # Calculate GDD for each crop
                    for crop, base_temp in crop_base_temps.items():
                        # GDD = (Daily Average Temperature - Base Temperature)
                        # GDD cannot be negative
                        gdd = max(0, daily_avg - base_temp)
                        daily_gdd[crop].append({
                            'date': record.date,
                            'gdd': gdd,
                            'temp_avg': daily_avg
                        })
                        cumulative_gdd[crop] += gdd
                
                except ValueError:
                    pass
        
        # Display GDD results
        print(f"\n📊 Growing Degree Days Summary:")
        print(f"   Period: {start_date} to {end_date}")
        print("-" * 40)
        
        for crop, base_temp in crop_base_temps.items():
            total_gdd = cumulative_gdd[crop]
            avg_daily_gdd = total_gdd / len(daily_gdd[crop]) if daily_gdd[crop] else 0
            
            print(f"\n🌾 {crop} (Base: {base_temp}°F)")
            print(f"   Cumulative GDD: {total_gdd:.1f}")
            print(f"   Average daily GDD: {avg_daily_gdd:.1f}")
            
            # Recent GDD activity (last 7 days)
            if len(daily_gdd[crop]) >= 7:
                recent_gdd = sum(d['gdd'] for d in daily_gdd[crop][-7:])
                print(f"   Last 7 days GDD: {recent_gdd:.1f}")
            
            # Development stage estimates (example for corn)
            if crop == 'Corn':
                if total_gdd < 100:
                    stage = "Emergence"
                elif total_gdd < 350:
                    stage = "Vegetative Growth"
                elif total_gdd < 850:
                    stage = "Reproductive Development"
                elif total_gdd < 1400:
                    stage = "Grain Filling"
                else:
                    stage = "Maturity"
                
                print(f"   Estimated stage: {stage}")
            
            # High GDD days (>20 GDD)
            high_gdd_days = len([d for d in daily_gdd[crop] if d['gdd'] > 20])
            print(f"   High GDD days (>20): {high_gdd_days}")
        
        # GDD comparison chart (text-based)
        print(f"\n📈 GDD Accumulation Comparison:")
        max_gdd = max(cumulative_gdd.values()) if cumulative_gdd.values() else 0
        
        for crop, total_gdd in cumulative_gdd.items():
            bar_length = int((total_gdd / max_gdd) * 30) if max_gdd > 0 else 0
            bar = "█" * bar_length + "░" * (30 - bar_length)
            print(f"   {crop:10} {bar} {total_gdd:.0f}")
    
    except Exception as e:
        print(f"Error: {e}")


def water_stress_analysis():
    """Analyze water stress conditions using ETo and precipitation data."""
    print("\n💧 Water Stress Analysis")
    print("=" * 50)
    
    client = CimisClient(app_key=os.getenv('CIMIS_API_KEY', 'your-api-key-here'))
    
    try:
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=45)  # 6+ weeks
        
        weather_data = client.get_daily_data(
            targets=[2],  # Five Points
            start_date=start_date,
            end_date=end_date,
            data_items=["day-eto", "day-precip", "day-air-tmp-max", "day-rel-hum-avg"]
        )
        
        records = weather_data.get_all_records()
        print(f"Analyzing water stress for {len(records)} days")
        
        # Calculate water balance and stress indicators
        daily_water_balance = []
        cumulative_deficit = 0
        stress_days = 0
        severe_stress_days = 0
        
        for record in records:
            eto_data = record.data_values.get('day-eto')
            precip_data = record.data_values.get('day-precip')
            temp_max_data = record.data_values.get('day-air-tmp-max')
            humidity_data = record.data_values.get('day-rel-hum-avg')
            
            daily_eto = 0
            daily_precip = 0
            temp_max = 0
            humidity = 0
            
            if eto_data and eto_data.value:
                try:
                    daily_eto = float(eto_data.value)
                except ValueError:
                    pass
            
            if precip_data and precip_data.value:
                try:
                    daily_precip = float(precip_data.value)
                except ValueError:
                    pass
            
            if temp_max_data and temp_max_data.value:
                try:
                    temp_max = float(temp_max_data.value)
                except ValueError:
                    pass
            
            if humidity_data and humidity_data.value:
                try:
                    humidity = float(humidity_data.value)
                except ValueError:
                    pass
            
            # Calculate daily water balance
            daily_balance = daily_precip - daily_eto
            cumulative_deficit += min(0, daily_balance)  # Only accumulate deficits
            
            # Stress indicators
            # High stress: ETo > 0.25", temp > 95°F, humidity < 30%
            # Moderate stress: ETo > 0.20", temp > 90°F, humidity < 40%
            
            stress_score = 0
            if daily_eto > 0.25:
                stress_score += 2
            elif daily_eto > 0.20:
                stress_score += 1
            
            if temp_max > 95:
                stress_score += 2
            elif temp_max > 90:
                stress_score += 1
            
            if humidity < 30:
                stress_score += 2
            elif humidity < 40:
                stress_score += 1
            
            stress_level = "None"
            if stress_score >= 5:
                stress_level = "Severe"
                severe_stress_days += 1
                stress_days += 1
            elif stress_score >= 3:
                stress_level = "Moderate"
                stress_days += 1
            elif stress_score >= 1:
                stress_level = "Mild"
            
            daily_water_balance.append({
                'date': record.date,
                'eto': daily_eto,
                'precip': daily_precip,
                'balance': daily_balance,
                'temp_max': temp_max,
                'humidity': humidity,
                'stress_score': stress_score,
                'stress_level': stress_level
            })
        
        # Analysis results
        total_eto = sum(d['eto'] for d in daily_water_balance)
        total_precip = sum(d['precip'] for d in daily_water_balance)
        total_deficit = total_eto - total_precip
        
        print(f"\n💧 Water Balance Summary:")
        print(f"   Total ETo: {total_eto:.2f} inches")
        print(f"   Total precipitation: {total_precip:.2f} inches")
        print(f"   Total water deficit: {total_deficit:.2f} inches")
        print(f"   Cumulative deficit: {abs(cumulative_deficit):.2f} inches")
        
        print(f"\n🌡️  Stress Analysis:")
        print(f"   Total stress days: {stress_days} ({stress_days/len(records)*100:.1f}%)")
        print(f"   Severe stress days: {severe_stress_days} ({severe_stress_days/len(records)*100:.1f}%)")
        
        # Recent stress pattern (last 7 days)
        if len(daily_water_balance) >= 7:
            recent_stress = daily_water_balance[-7:]
            recent_stress_days = len([d for d in recent_stress if d['stress_score'] >= 3])
            recent_deficit = sum(min(0, d['balance']) for d in recent_stress)
            
            print(f"\n📅 Recent Week Analysis:")
            print(f"   Stress days: {recent_stress_days}/7")
            print(f"   Week deficit: {abs(recent_deficit):.2f} inches")
            
            if recent_stress_days >= 5:
                print("   ⚠️  HIGH STRESS WEEK - Immediate irrigation recommended")
            elif recent_stress_days >= 3:
                print("   ⚠️  MODERATE STRESS - Monitor closely")
            else:
                print("   ✅ Manageable stress levels")
        
        # Worst stress days
        worst_days = sorted(daily_water_balance, key=lambda x: x['stress_score'], reverse=True)[:5]
        
        print(f"\n🔥 Highest Stress Days:")
        for i, day in enumerate(worst_days, 1):
            if day['stress_score'] > 0:
                print(f"   {i}. {day['date']}: {day['stress_level']} stress")
                print(f"      ETo: {day['eto']:.3f}\", Temp: {day['temp_max']:.0f}°F, Humidity: {day['humidity']:.0f}%")
        
        # Irrigation recommendations
        print(f"\n🚿 Irrigation Recommendations:")
        
        if abs(cumulative_deficit) > 2.0:
            print("   🚨 CRITICAL: Deep irrigation needed immediately")
        elif abs(cumulative_deficit) > 1.0:
            print("   ⚠️  HIGH: Increase irrigation frequency")
        elif abs(cumulative_deficit) > 0.5:
            print("   ⚠️  MODERATE: Monitor and adjust irrigation")
        else:
            print("   ✅ Current irrigation appears adequate")
        
        # Weekly irrigation schedule suggestion
        weekly_deficit = total_deficit / (len(records) / 7)
        print(f"   Suggested weekly irrigation: {weekly_deficit:.2f} inches")
    
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all data analysis examples."""
    print("📊 Python CIMIS Client - Data Analysis Examples")
    print("=" * 60)
    
    statistical_analysis()
    time_series_analysis()
    comparative_analysis()
    growing_degree_days()
    water_stress_analysis()
    
    print("\n✅ All data analysis examples completed!")
    print("\n🔬 Analysis Tips:")
    print("- Combine multiple data points for robust analysis")
    print("- Consider soil type and crop coefficients for accuracy")
    print("- Use quality control flags to filter unreliable data")
    print("- Implement statistical significance testing for trends")
    print("- Store results in databases for long-term pattern analysis")


if __name__ == "__main__":
    main()
