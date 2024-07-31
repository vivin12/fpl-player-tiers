import requests
import pandas as pd

# Fetch FPL data
fpl_api_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
response = requests.get(fpl_api_url)
data = response.json()

players = data['elements']
teams = {team['id']: team['name'] for team in data['teams']}

player_data = []
for player in players:
    player_data.append({
        'name': player['web_name'],
        'team': teams[player['team']],
        'total_points': player['total_points'],
        'value': player['now_cost'] / 10
    })

# Convert to DataFrame
df = pd.DataFrame(player_data)

# Create tiers based on total points
def assign_tier(points):
    if points >= 150:
        return 'S'
    elif points >= 100:
        return 'A'
    elif points >= 50:
        return 'B'
    else:
        return 'C'

df['tier'] = df['total_points'].apply(assign_tier)

# Save to CSV and JSON
df.to_csv('fpl_players_tiers.csv', index=False)
df.to_json('fpl_players_tiers.json', orient='records')

