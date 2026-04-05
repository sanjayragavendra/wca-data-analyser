"""
Country performance analysis module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class CountryAnalyzer:
    """Analyze country-specific performance"""
   
    def __init__(self, data, competitor_analyzer):
        self.data = data
        self.competitor_analyzer = competitor_analyzer
   
    def analyze_country(self, country_id):
        """Analyze a specific country"""
        # Find country
        country_match = self.data['countries'][
            (self.data['countries']['id'].str.contains(country_id, case=False, na=False)) |
            (self.data['countries']['name'].str.contains(country_id, case=False, na=False))
        ]
       
        if country_match.empty:
            print(f"❌ Country '{country_id}' not found")
            return
       
        country = country_match.iloc[0]
        print(f"\n📊 ANALYZING: {country['name']} ({country['id']})")
       
        # Get country results
        country_results = self.competitor_analyzer.get_country_results(country['id'])
       
        if country_results.empty:
            print("❌ No results found for this country")
            return
       
        print(f"\n   Total results: {len(country_results):,}")
        print(f"   Unique competitors: {country_results['person_id'].nunique():,}")
        print(f"   Unique competitions: {country_results['competition_id'].nunique():,}")
       
        # Best events
        print(f"\n🎯 BEST PERFORMANCES BY EVENT:")
        for event_id in ['333', '222', '444', '555', '666', '777']:
            event_results = country_results[country_results['event_id'] == event_id]
            if not event_results.empty and 'average_seconds' in event_results.columns:
                best_time = event_results['average_seconds'].min()
                event_name = self.competitor_analyzer.event_names.get(event_id, event_id)
                print(f"   {event_name}: {best_time:.2f}s")
       
        # Plot country performance
        self.plot_country_performance(country, country_results)
   
    def plot_country_performance(self, country, country_results):
        """Plot country performance charts"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'{country["name"]} Performance Analysis', fontsize=14, fontweight='bold')
       
        # 1. Top competitors in country
        top_comp = country_results.groupby('person_id')['average_seconds'].min().nsmallest(10)
        axes[0,0].barh(range(len(top_comp)), top_comp.values, color='#2E86AB')
        axes[0,0].set_yticks(range(len(top_comp)))
        axes[0,0].set_yticklabels([f"Competitor {i+1}" for i in range(len(top_comp))])
        axes[0,0].set_xlabel('Best Time (seconds)')
        axes[0,0].set_title(f'Top 10 Competitors')
        axes[0,0].grid(True, alpha=0.3)
       
        # 2. Event participation
        event_participation = country_results['event_id'].value_counts().head(8)
        axes[0,1].bar(event_participation.index, event_participation.values, color='#A23B72')
        axes[0,1].set_xlabel('Event')
        axes[0,1].set_ylabel('Number of Results')
        axes[0,1].set_title('Event Participation')
        axes[0,1].tick_params(axis='x', rotation=45)
       
        # 3. Yearly participation
        yearly_part = country_results.groupby('year')['person_id'].nunique()
        axes[1,0].plot(yearly_part.index, yearly_part.values, marker='o', color='#F18F01', linewidth=2)
        axes[1,0].set_xlabel('Year')
        axes[1,0].set_ylabel('Active Competitors')
        axes[1,0].set_title('Active Competitors Over Time')
        axes[1,0].grid(True, alpha=0.3)
       
        # 4. Time distribution for main event
        main_event = country_results[country_results['event_id'] == '333']
        if not main_event.empty:
            axes[1,1].hist(main_event['average_seconds'], bins=30, edgecolor='black', alpha=0.7, color='#C73E1D')
            axes[1,1].set_xlabel('Time (seconds)')
            axes[1,1].set_ylabel('Frequency')
            axes[1,1].set_title('3x3 Time Distribution')
            axes[1,1].axvline(main_event['average_seconds'].median(), color='red',
                             linestyle='--', label=f'Median: {main_event["average_seconds"].median():.2f}s')
            axes[1,1].legend()
       
        plt.tight_layout()
        plt.show()
