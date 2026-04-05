"""
Plotting and visualization utilities
"""
import pandas as pd  # Add this line
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


class Plotter:
    """Handles all visualization tasks"""
   
    def plot_event_performance(self, results, event_id, competitor_name, event_names):
        """Create separate window for single and average performance for an event with labeled points"""
        event_name = event_names.get(event_id, event_id)
        event_results = results[results['event_id'] == event_id].sort_values('year')
       
        if event_results.empty:
            return
       
        # Create figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'{competitor_name} - {event_name} Performance Analysis', fontsize=14, fontweight='bold')
       
        # Filter valid times
        if 'best_seconds' in event_results.columns:
            best_times = event_results[event_results['best_seconds'].notna() &
                                      (event_results['best_seconds'] > 0) &
                                      (event_results['best_seconds'] < 600)].copy()
        else:
            best_times = pd.DataFrame()
       
        if 'average_seconds' in event_results.columns:
            avg_times = event_results[event_results['average_seconds'].notna() &
                                     (event_results['average_seconds'] > 0) &
                                     (event_results['average_seconds'] < 600)].copy()
        else:
            avg_times = pd.DataFrame()
       
        # Plot 1: Single/Best times with labeled points
        if not best_times.empty:
            years_best = best_times['year'].values
            times_best = best_times['best_seconds'].values
           
            # Plot line
            ax1.plot(years_best, times_best, '-', linewidth=1.5, color='#2E86AB', alpha=0.5)
           
            # Plot points with numbers
            for i, (year, time) in enumerate(zip(years_best, times_best)):
                ax1.plot(year, time, 'o', markersize=8, color='#2E86AB',
                        markeredgecolor='white', markeredgewidth=1)
                ax1.annotate(str(i+1), (year, time), textcoords="offset points",
                            xytext=(0,10), ha='center', fontsize=9, fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
           
            # Add trend line for best times
            if len(times_best) >= 3:
                z_best = np.polyfit(years_best, times_best, 1)
                p_best = np.poly1d(z_best)
                ax1.plot(years_best, p_best(years_best), '--', color='#2E86AB',
                        alpha=0.5, label=f'Trend: {-z_best[0]:.2f}s/year')
           
            # Highlight best ever
            best_idx = np.argmin(times_best)
            ax1.plot(years_best[best_idx], times_best[best_idx], '*', markersize=15,
                    color='gold', markeredgecolor='black', markeredgewidth=1,
                    label=f'PB: {times_best[best_idx]:.2f}s')
           
            # Add improvement rate text
            # Note: This requires access to calculate_improvement_rate method
            # We'll handle this in the competitor analyzer
            pass
       
        ax1.set_xlabel('Year', fontsize=11)
        ax1.set_ylabel('Time (seconds)', fontsize=11)
        ax1.set_title('Single/Best Times (Numbered Points)', fontsize=12, fontweight='bold')
        ax1.legend(loc='best', fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(bottom=0)
       
        # Create legend for best times points
        if not best_times.empty:
            legend_text = "Best Times:\n"
            for i, (_, row) in enumerate(best_times.iterrows()):
                comp_name = row.get('competition_id', 'Unknown')[:10]
                year = int(row['year']) if pd.notna(row['year']) else 'Unknown'
                time = row['best_seconds']
                legend_text += f"{i+1}. {comp_name} ({year}): {time:.2f}s\n"
           
            ax1.text(1.02, 0.98, legend_text, transform=ax1.transAxes, fontsize=8,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
       
        # Plot 2: Average times with labeled points
        if not avg_times.empty:
            years_avg = avg_times['year'].values
            times_avg = avg_times['average_seconds'].values
           
            # Plot line
            ax2.plot(years_avg, times_avg, '-', linewidth=1.5, color='#A23B72', alpha=0.5)
           
            # Plot points with numbers
            for i, (year, time) in enumerate(zip(years_avg, times_avg)):
                ax2.plot(year, time, 's', markersize=8, color='#A23B72',
                        markeredgecolor='white', markeredgewidth=1)
                ax2.annotate(str(i+1), (year, time), textcoords="offset points",
                            xytext=(0,10), ha='center', fontsize=9, fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
           
            # Add trend line for average times
            if len(times_avg) >= 3:
                z_avg = np.polyfit(years_avg, times_avg, 1)
                p_avg = np.poly1d(z_avg)
                ax2.plot(years_avg, p_avg(years_avg), '--', color='#A23B72',
                        alpha=0.5, label=f'Trend: {-z_avg[0]:.2f}s/year')
           
            # Highlight best average
            best_avg_idx = np.argmin(times_avg)
            ax2.plot(years_avg[best_avg_idx], times_avg[best_avg_idx], '*', markersize=15,
                    color='gold', markeredgecolor='black', markeredgewidth=1,
                    label=f'Best Avg: {times_avg[best_avg_idx]:.2f}s')
       
        ax2.set_xlabel('Year', fontsize=11)
        ax2.set_ylabel('Time (seconds)', fontsize=11)
        ax2.set_title('Average Times (Numbered Points)', fontsize=12, fontweight='bold')
        ax2.legend(loc='best', fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(bottom=0)
       
        # Create legend for average times points
        if not avg_times.empty:
            legend_text = "Average Times:\n"
            for i, (_, row) in enumerate(avg_times.iterrows()):
                comp_name = row.get('competition_id', 'Unknown')[:10]
                year = int(row['year']) if pd.notna(row['year']) else 'Unknown'
                time = row['average_seconds']
                legend_text += f"{i+1}. {comp_name} ({year}): {time:.2f}s\n"
           
            ax2.text(1.02, 0.98, legend_text, transform=ax2.transAxes, fontsize=8,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightpink', alpha=0.8))
       
        plt.tight_layout()
        plt.show()
   
    def plot_podium_pie_charts(self, wca_id, event_id, competitor_name, analyzer, event_names):
        """Create pie charts with legends for podium history and next event probability"""
        event_name = event_names.get(event_id, event_id)
       
        # Get podium data for this specific event
        prob, podium_count, total_comps, avg_podium_time = analyzer.predict_podium_probability(wca_id, event_id)
       
        if not isinstance(prob, (int, float)) or total_comps == 0:
            return
       
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'{competitor_name} - {event_name} Podium Analysis', fontsize=14, fontweight='bold')
       
        # Pie Chart 1: Historical Podium Finishes with Legend
        labels1 = ['🏆 Podium Finishes', '❌ Non-Podium']
        sizes1 = [podium_count, total_comps - podium_count]
        colors1 = ['#2E86AB', '#A23B72']
        explode1 = (0.1, 0)  # Explode the podium slice
       
        wedges1, texts1, autotexts1 = ax1.pie(sizes1, explode=explode1, colors=colors1,
                                              autopct='%1.1f%%', startangle=90, shadow=True,
                                              textprops={'fontsize': 10})
       
        # Add legend for first pie chart
        ax1.legend(wedges1, labels1, title="Podium History", loc="center left",
                   bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
       
        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
       
        ax1.set_title('Historical Podium Performance', fontweight='bold', fontsize=11)
        ax1.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
       
        # Add text box with details
        podium_percentage = (podium_count / total_comps) * 100 if total_comps > 0 else 0
        ax1.text(0, -1.4, f"📊 Statistics:\n• Total Competitions: {total_comps}\n• Podium Finishes: {podium_count}\n• Podium Rate: {podium_percentage:.1f}%",
                ha='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='gray', alpha=0.9))
       
        # Pie Chart 2: Next Event Podium Probability with Legend
        next_podium_prob = prob
        next_non_podium = 100 - next_podium_prob
       
        labels2 = ['✅ Podium Chance', '⬜ Non-Podium Chance']
        sizes2 = [next_podium_prob, next_non_podium]
        colors2 = ['#F18F01', '#C73E1D']
        explode2 = (0.1, 0)
       
        wedges2, texts2, autotexts2 = ax2.pie(sizes2, explode=explode2, colors=colors2,
                                              autopct='%1.1f%%', startangle=90, shadow=True,
                                              textprops={'fontsize': 10})
       
        # Add legend for second pie chart
        ax2.legend(wedges2, labels2, title="Next Event Prediction", loc="center left",
                   bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
       
        for autotext in autotexts2:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
       
        ax2.set_title('Next Event Podium Prediction', fontweight='bold', fontsize=11)
        ax2.axis('equal')
       
        # Get improvement trend
        results = analyzer.get_competitor_results(wca_id)
        best_impr, _, _, _ = analyzer.calculate_improvement_rate(results, event_id, use_best=True)
        avg_impr, _, _, _ = analyzer.calculate_improvement_rate(results, event_id, use_best=False)
        future_best, best_conf = analyzer.predict_future_time(results, event_id, years_ahead=1, use_best=True)
       
        # Add text box with prediction details
        trend_text = f"🔮 Prediction Details:\n• Probability: {next_podium_prob:.1f}%\n"
        if best_impr > 0:
            trend_text += f"• Improvement: {best_impr:.2f}s/year\n"
        if future_best is not None:
            trend_text += f"• Predicted Best: {future_best:.2f}s"
        else:
            trend_text += "• Insufficient data for time prediction"
       
        ax2.text(0, -1.4, trend_text, ha='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='gray', alpha=0.9))
       
        plt.tight_layout()
        plt.subplots_adjust(right=0.85)  # Make room for legends
        plt.show()
   
    def plot_podium_summary(self, wca_id, podium_predictions, competitor_name):
        """Create separate window for overall podium summary with legends"""
        if not podium_predictions:
            return
       
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle(f'{competitor_name} - Overall Podium Analysis', fontsize=14, fontweight='bold')
       
        # Podium probability bar chart with better styling
        events = [p['event'] for p in podium_predictions]
        probs = [p['probability'] for p in podium_predictions]
       
        # Sort by probability
        sorted_idx = np.argsort(probs)
        events = [events[i] for i in sorted_idx]
        probs = [probs[i] for i in sorted_idx]
       
        # Create color map based on probability
        colors = ['#FF6B6B' if p < 30 else '#FFD93D' if p < 60 else '#6BCB77' for p in probs]
       
        bars = ax1.barh(events, probs, color=colors, edgecolor='black', linewidth=0.5)
        ax1.set_xlabel('Podium Probability (%)', fontsize=11)
        ax1.set_title('Podium Probability by Event', fontweight='bold', fontsize=12)
        ax1.set_xlim(0, 100)
       
        # Add value labels
        for bar, prob in zip(bars, probs):
            ax1.text(prob + 1, bar.get_y() + bar.get_height()/2, f'{prob:.1f}%',
                    va='center', fontweight='bold', fontsize=9)
       
        # Add legend for probability colors
        legend_elements = [
            Patch(facecolor='#6BCB77', label='High (≥60%)'),
            Patch(facecolor='#FFD93D', label='Medium (30-60%)'),
            Patch(facecolor='#FF6B6B', label='Low (<30%)')
        ]
        ax1.legend(handles=legend_elements, title='Probability Level',
                   loc='lower right', fontsize=8)
       
        ax1.grid(True, alpha=0.3, axis='x')
       
        # Podium finishes pie chart for top event with legend
        if podium_predictions:
            top_event = max(podium_predictions, key=lambda x: x['probability'])
            labels2 = ['🏆 Podium Finishes', '❌ Non-Podium']
            sizes2 = [top_event['podium_count'], top_event['total_comps'] - top_event['podium_count']]
            colors2 = ['#2E86AB', '#A23B72']
            explode2 = (0.1, 0)
           
            wedges2, texts2, autotexts2 = ax2.pie(sizes2, explode=explode2, colors=colors2,
                                                  autopct='%1.1f%%', startangle=90, shadow=True,
                                                  textprops={'fontsize': 10})
           
            # Add legend for the pie chart
            ax2.legend(wedges2, labels2, title=f"{top_event['event'][:20]}",
                       loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
           
            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
           
            ax2.set_title(f"Podium History - {top_event['event']}", fontweight='bold', fontsize=11)
            ax2.axis('equal')
           
            # Add text with counts
            podium_percentage = (top_event['podium_count'] / top_event['total_comps']) * 100
            ax2.text(0, -1.3, f"📊 Statistics:\n• Total: {top_event['total_comps']}\n• Podium: {top_event['podium_count']}\n• Rate: {podium_percentage:.1f}%",
                    ha='center', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='gray', alpha=0.9))
       
        plt.tight_layout()
        plt.subplots_adjust(right=0.85)  # Make room for legends
        plt.show()
