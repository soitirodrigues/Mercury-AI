import json
import os
import pandas as pd

def calculate_statistics(results_dir: str = "data/replay_results"):
    results = []
    
    # Load all json results
    for filename in os.listdir(results_dir):
        if filename.endswith(".json"):
            with open(os.path.join(results_dir, filename), 'r') as f:
                results.append(json.load(f))
    
    if not results:
        print("No results found.")
        return

    df = pd.DataFrame(results)
    
    stats = {}
    
    # Accuracy per decision
    for decision in ['BUY', 'SELL', 'WAIT']:
        subset = df[df['decision'] == decision]
        if not subset.empty:
            stats[f'{decision}_accuracy'] = subset['hit'].mean()
        else:
            stats[f'{decision}_accuracy'] = 0.0
            
    # Additional metrics
    stats['avg_confidence'] = df['confidence'].mean()
    stats['total_signals'] = len(df)
    
    print(json.dumps(stats, indent=4))

if __name__ == "__main__":
    calculate_statistics()
