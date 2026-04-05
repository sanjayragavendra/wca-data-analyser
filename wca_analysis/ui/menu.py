"""
Main menu system for WCA analysis
"""

from wca_analysis.data.data_loader import WCADataLoader
from wca_analysis.analysis.competitor_analyzer import CompetitorAnalyzer
from wca_analysis.analysis.global_analyzer import GlobalAnalyzer
from wca_analysis.analysis.country_analyzer import CountryAnalyzer
from wca_analysis.analysis.event_analyzer import EventAnalyzer
from wca_analysis.models.predictive_models import PredictiveModels
from wca_analysis.models.clustering import CompetitorClustering


class WCAMenu:
    """Main menu system for WCA analysis"""
   
    def __init__(self):
        self.loader = WCADataLoader()
        self.data = None
        self.competitor_analyzer = None
        self.global_analyzer = None
        self.country_analyzer = None
        self.event_analyzer = None
        self.predictive_models = None
        self.clustering = None
       
    def initialize(self):
        """Load data and initialize analyzers"""
        print("\n" + "="*60)
        print("🚀 WCA DATA ANALYSIS AND PREDICTION SUITE")
        print("="*60)
       
        self.data = self.loader.load_all_files()
        self.data = self.loader.preprocess_data()
       
        self.competitor_analyzer = CompetitorAnalyzer(self.data)
        self.global_analyzer = GlobalAnalyzer(self.data)
        self.country_analyzer = CountryAnalyzer(self.data, self.competitor_analyzer)
        self.event_analyzer = EventAnalyzer(self.data, self.competitor_analyzer)
        self.predictive_models = PredictiveModels(self.data, self.competitor_analyzer)
        self.clustering = CompetitorClustering(self.data, self.competitor_analyzer)
       
        print("\n✅ System ready!")
   
    def show_main_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("📊 MAIN MENU")
        print("="*60)
        print("1. 🔍 Analyze Competitor by WCA ID")
        print("2. 📈 Global Statistics & Trends")
        print("3. 🌍 Country Performance Analysis")
        print("4. 🎯 Event Performance Analysis")
        print("5. 🤖 Predictive Models")
        print("6. ❌ Exit")
        print("-"*60)
   
    def run(self):
        """Run the menu system"""
        self.initialize()
       
        while True:
            self.show_main_menu()
           
            try:
                choice = input("👉 Enter your choice (1-6): ").strip()
               
                if choice == '1':
                    self.analyze_competitor_menu()
                elif choice == '2':
                    self.global_statistics_menu()
                elif choice == '3':
                    self.country_analysis_menu()
                elif choice == '4':
                    self.event_analysis_menu()
                elif choice == '5':
                    self.predictive_models_menu()
                elif choice == '6':
                    print("\n👋 Thank you for using WCA Analysis Suite! Goodbye!")
                    break
                else:
                    print("\n❌ Invalid choice. Please enter 1-6.")
                   
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
   
    def analyze_competitor_menu(self):
        """Competitor analysis menu"""
        print("\n" + "="*60)
        print("🔍 COMPETITOR ANALYSIS")
        print("="*60)
       
        wca_id = input("Enter WCA ID (e.g., 2003BELL01): ").strip().upper()
       
        if not wca_id:
            print("❌ No WCA ID entered.")
            return
       
        self.competitor_analyzer.analyze_competitor(wca_id)
       
        input("\nPress Enter to continue...")
   
    def global_statistics_menu(self):
        """Global statistics menu"""
        print("\n" + "="*60)
        print("📈 GLOBAL STATISTICS & TRENDS")
        print("="*60)
       
        if self.data['results'].empty:
            print("❌ No results data available")
            return
       
        self.global_analyzer.analyze_global_stats()
       
        input("\nPress Enter to continue...")
   
    def country_analysis_menu(self):
        """Country analysis menu"""
        print("\n" + "="*60)
        print("🌍 COUNTRY PERFORMANCE ANALYSIS")
        print("="*60)
       
        if 'countries' not in self.data or self.data['countries'].empty:
            print("❌ Countries data not available")
            return
       
        # Show available countries
        print("\n📋 TOP 20 COUNTRIES BY PARTICIPATION:")
        if 'results' in self.data and 'country_id' in self.data['results'].columns:
            country_counts = self.data['results']['country_id'].value_counts().head(20)
            for i, (country_id, count) in enumerate(country_counts.items(), 1):
                country_name = self.data['countries'][self.data['countries']['id'] == country_id]['name'].values
                country_name = country_name[0] if len(country_name) > 0 else country_id
                print(f"   {i}. {country_name}: {count:,} results")
       
        country_id = input("\nEnter country code or name: ").strip()
       
        if not country_id:
            return
       
        self.country_analyzer.analyze_country(country_id)
       
        input("\nPress Enter to continue...")
   
    def event_analysis_menu(self):
        """Event analysis menu"""
        print("\n" + "="*60)
        print("🎯 EVENT PERFORMANCE ANALYSIS")
        print("="*60)
       
        if 'events' not in self.data or self.data['events'].empty:
            print("❌ Events data not available")
            return
       
        # Show available events
        print("\n📋 AVAILABLE EVENTS:")
        for _, row in self.data['events'].iterrows():
            print(f"   {row['id']}: {row['name']}")
       
        event_id = input("\nEnter event ID (e.g., 333, 222, 444): ").strip()
       
        if not event_id:
            return
       
        self.event_analyzer.analyze_event(event_id)
       
        input("\nPress Enter to continue...")
   
    def predictive_models_menu(self):
        """Predictive models menu"""
        print("\n" + "="*60)
        print("🤖 PREDICTIVE MODELS")
        print("="*60)
       
        print("\n1. Forecast World Records (Linear Regression)")
        print("2. Cluster Competitors by Performance (K-Means)")
        print("3. Back to Main Menu")
       
        choice = input("\nEnter choice: ").strip()
       
        if choice == '1':
            event_id = input("Enter event ID to forecast (default: 333): ").strip() or '333'
            self.predictive_models.forecast_world_records(event_id)
            input("\nPress Enter to continue...")
        elif choice == '2':
            event_id = input("Enter event ID to cluster (default: 333): ").strip() or '333'
            self.clustering.cluster_competitors(event_id)
            input("\nPress Enter to continue...")
