"""
Event performance analysis module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class EventAnalyzer:
    """Analyze specific event performance"""
   
    def __init__(self, data, competitor_analyzer):
        self.data = data
        self.competitor_analyzer = competitor_analyzer
   
    def analyze_event(self, event_id):
        """Analyze a specific event"""
        event_name = self.competitor_analyzer.event_names.get(event_id, event_id)
       
        # Get event results
        if 'results' not in self.data:
            print("❌ Results data not available")
            return
       
        event_results = self.data['results'][
            (self.data['results']['event_id'] == event_id) &
            (self.data['results']['average_seconds'].notna()) &
            (self.data['results']['average_seconds'] < 300)
        ]
       
        if event_results.empty:
            print(f"❌ No results found for event {event_name}")
            return
       
        print(f"\n📊 {event_name} STATISTICS:")
        print(f"   Total results: {len(event_results):,}")
        print(f"   Unique competitors: {event_results['person_id'].nunique():,}")
        print(f"   World Record: {event_results['average_seconds'].min():.2f}s")
        print(f"   Median time: {event_results['average_seconds'].median():.2f}s")
        print(f"   Average time: {event_results['average_seconds'].mean():.2f}s")
        print(f"   Standard deviation: {event_results['average_seconds'].std():.2f}s")
       
        # Percentiles
        percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        print(f"\n📈 PERCENTILES:")
        for p in percentiles:
            print(f"   {p}th percentile: {event_results['average_seconds'].quantile(p/100):.2f}s")
       
        # Plot distribution
        self.plot_event_distribution(event_id, event_name, event_results)
   
    def plot_event_distribution(self, event_id, event_name, event_results):
        """Plot event distribution charts"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'{event_name} Analysis', fontsize=14, fontweight='bold')
       
        # 1. Time distribution
        axes[0,0].hist(event_results['average_seconds'], bins=50, edgecolor='black', alpha=0.7, color='#2E86AB')
        axes[0,0].set_xlabel('Time (seconds)')
        axes[0,0].set_ylabel('Frequency')
        axes[0,0].set_title('Time Distribution')
        axes[0,0].axvline(event_results['average_seconds'].median(), color='red',
                         linestyle='--', label=f'Median: {event_results["average_seconds"].median():.2f}s')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
       
        # 2. Box plot by year
        if 'year' in event_results.columns:
            recent_years = event_results[event_results['year'] >= 2015]
            if not recent_years.empty:
                recent_years.boxplot(column='average_seconds', by='year', ax=axes[0,1])
                axes[0,1].set_title('Times by Year')
                axes[0,1].set_xlabel('Year')
                axes[0,1].set_ylabel('Time (seconds)')
                axes[0,1].tick_params(axis='x', rotation=45)
       
        # 3. Performance over time
        if 'year' in event_results.columns:
            yearly_stats = event_results.groupby('year')['average_seconds'].agg(['mean', 'median', 'min'])
            axes[1,0].plot(yearly_stats.index, yearly_stats['mean'], 'o-', label='Mean', linewidth=2, color='#2E86AB')
            axes[1,0].plot(yearly_stats.index, yearly_stats['median'], 's-', label='Median', linewidth=2, color='#A23B72')
            axes[1,0].plot(yearly_stats.index, yearly_stats['min'], '^-', label='Best', linewidth=2, color='#F18F01')
            axes[1,0].set_xlabel('Year')
            axes[1,0].set_ylabel('Time (seconds)')
            axes[1,0].set_title('Performance Over Time')
            axes[1,0].legend()
            axes[1,0].grid(True, alpha=0.3)
       
        # 4. Top countries for this event
        if 'country_id' in event_results.columns:
            country_stats = event_results.groupby('country_id').agg({
                'average_seconds': 'median',
                'person_id': 'nunique'
            }).reset_index()
            top_countries = country_stats.nsmallest(10, 'average_seconds')
           
            # Get country names
            if 'countries' in self.data and not self.data['countries'].empty:
                country_names = []
                for cid in top_countries['country_id']:
                    name = self.data['countries'][self.data['countries']['id'] == cid]['name'].values
                    country_names.append(name[0][:15] + '...' if len(name[0]) > 15 else name[0] if len(name) > 0 else cid)
            else:
                country_names = top_countries['country_id']
           
            axes[1,1].barh(range(len(top_countries)), top_countries['average_seconds'], color='#C73E1D')
            axes[1,1].set_yticks(range(len(top_countries)))
            axes[1,1].set_yticklabels(country_names)
            axes[1,1].set_xlabel('Median Time (seconds)')
            axes[1,1].set_title('Top 10 Countries by Median Time')
            axes[1,1].grid(True, alpha=0.3)
       
        plt.tight_layout()
        plt.show()
