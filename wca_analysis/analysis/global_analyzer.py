"""
Global statistics analysis module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class GlobalAnalyzer:
    """Analyze global WCA statistics and trends"""
   
    def __init__(self, data):
        self.data = data
   
    def analyze_global_stats(self):
        """Generate global statistics"""
        if self.data['results'].empty:
            print("❌ No results data available")
            return
       
        results = self.data['results']
       
        # Basic stats
        print(f"\n📊 DATASET OVERVIEW:")
        print(f"   Total results: {len(results):,}")
        print(f"   Unique competitors: {results['person_id'].nunique():,}")
        print(f"   Unique competitions: {results['competition_id'].nunique():,}")
        print(f"   Year range: {int(results['year'].min()) if results['year'].notna().any() else 'N/A'} - {int(results['year'].max()) if results['year'].notna().any() else 'N/A'}")
       
        # Event distribution
        if 'events' in self.data and not self.data['events'].empty:
            event_names = dict(zip(self.data['events']['id'], self.data['events']['name']))
            print(f"\n🎯 TOP EVENTS BY PARTICIPATION:")
            event_counts = results['event_id'].value_counts().head(5)
            for event_id, count in event_counts.items():
                event_name = event_names.get(event_id, event_id)
                print(f"   {event_name}: {count:,} results")
       
        # Plot global trends
        self.plot_global_trends()
   
    def plot_global_trends(self):
        """Plot global trends"""
        results = self.data['results']
        event_names = dict(zip(self.data['events']['id'], self.data['events']['name'])) if 'events' in self.data else {}
       
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Global WCA Statistics', fontsize=14, fontweight='bold')
       
        # 1. Participation over time
        yearly_comp = results.groupby('year')['competition_id'].nunique()
        yearly_comp.plot(ax=axes[0,0], marker='o', color='#2E86AB')
        axes[0,0].set_title('Competitions per Year')
        axes[0,0].set_xlabel('Year')
        axes[0,0].set_ylabel('Number of Competitions')
        axes[0,0].grid(True, alpha=0.3)
       
        # 2. Average times over time (3x3)
        if 'average_seconds' in results.columns:
            threeby3 = results[results['event_id'] == '333']
            if not threeby3.empty:
                yearly_avg = threeby3.groupby('year')['average_seconds'].median()
                yearly_avg.plot(ax=axes[0,1], marker='o', color='#A23B72')
                axes[0,1].set_title('Median 3x3 Time Over Years')
                axes[0,1].set_xlabel('Year')
                axes[0,1].set_ylabel('Time (seconds)')
                axes[0,1].grid(True, alpha=0.3)
       
        # 3. Top countries
        if 'country_id' in results.columns:
            top_countries = results['country_id'].value_counts().head(10)
            top_countries.plot(kind='bar', ax=axes[1,0], color='#F18F01')
            axes[1,0].set_title('Top 10 Countries by Participation')
            axes[1,0].set_xlabel('Country')
            axes[1,0].set_ylabel('Number of Results')
            axes[1,0].tick_params(axis='x', rotation=45)
       
        # 4. Time distribution
        if 'average_seconds' in results.columns:
            times = results[results['average_seconds'] < 60]['average_seconds']
            axes[1,1].hist(times, bins=50, edgecolor='black', alpha=0.7, color='#C73E1D')
            axes[1,1].set_title('Distribution of Solve Times (<60s)')
            axes[1,1].set_xlabel('Time (seconds)')
            axes[1,1].set_ylabel('Frequency')
            axes[1,1].axvline(times.median(), color='red', linestyle='--',
                             label=f'Median: {times.median():.2f}s')
            axes[1,1].legend()
       
        plt.tight_layout()
        plt.show()
