"""
Data loading and preprocessing for WCA export files
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class WCADataLoader:
    """Load and preprocess all WCA data files"""
   
    def __init__(self, data_path='./'):
        self.data_path = data_path
        self.data = {}
        self.event_names = {}
       
    def load_all_files(self):
        """Load all TSV files"""
        print("\n📂 Loading WCA data files...")
       
        file_configs = {
            'persons': {'file': 'WCA_export_persons.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'results': {'file': 'WCA_export_results.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'ranks_average': {'file': 'WCA_export_ranks_average.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'events': {'file': 'WCA_export_events.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'countries': {'file': 'WCA_export_countries.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'continents': {'file': 'WCA_export_continents.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'round_types': {'file': 'WCA_export_round_types.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'scrambles': {'file': 'WCA_export_scrambles.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'result_attempts': {'file': 'WCA_export_result_attempts.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'competitions': {'file': 'WCA_export_competitions.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'championships': {'file': 'WCA_export_championships.tsv', 'sep': '\t', 'encoding': 'utf-8'},
            'formats': {'file': 'WCA_export_formats.tsv', 'sep': '\t', 'encoding': 'utf-8'}
        }
       
        for key, config in file_configs.items():
            try:
                df = pd.read_csv(
                    f"{self.data_path}{config['file']}",
                    sep=config['sep'],
                    encoding=config['encoding'],
                    low_memory=False,
                    on_bad_lines='skip'
                )
                self.data[key] = df
                print(f"  ✅ Loaded {key}: {len(df):,} records")
            except Exception as e:
                print(f"  ❌ Error loading {key}: {str(e)}")
                self.data[key] = pd.DataFrame()
       
        # Create event name mapping
        if 'events' in self.data and not self.data['events'].empty:
            self.event_names = dict(zip(self.data['events']['id'], self.data['events']['name']))
       
        return self.data
   
    def preprocess_data(self):
        """Clean and preprocess the loaded data"""
        print("\n🔄 Preprocessing data...")
       
        if 'results' in self.data and not self.data['results'].empty:
            # Convert time fields from centiseconds to seconds
            for col in ['best', 'average']:
                if col in self.data['results'].columns:
                    self.data['results'][f'{col}_seconds'] = self.data['results'][col] / 100
                    # Handle DNF, DNS etc.
                    mask = self.data['results'][col] > 99999999
                    self.data['results'].loc[mask, f'{col}_seconds'] = np.nan
                    self.data['results'].loc[self.data['results'][f'{col}_seconds'] < 0, f'{col}_seconds'] = np.nan
           
            # Extract year from competition IDs
            if 'competition_id' in self.data['results'].columns:
                # Extract 4-digit year using string slicing
                self.data['results']['year'] = self.data['results']['competition_id'].str.extract(r'(\d{4})').astype(float)
                self.data['results'].loc[self.data['results']['year'] < 2000, 'year'] = np.nan
       
        print("✅ Preprocessing complete!")
        return self.data
