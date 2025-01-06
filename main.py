# -*- coding: utf-8 -*-
"""
@author: Gil Sorek

GW Summary for Fantasy Premier-League (FPL)
"""

import requests
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
        
def get_player_webname(id): return players_stats[id]['web_name']
def get_team_name(id): return team_name[id]
def get_chip_name(chip): return {'bboost': "Bench-Boost", 'freehit': "Free-Hit", 'wildcard': "Wildcard", '3xc': "Triple-Captain"}[chip]
def element_type_to_pos(type): return {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}[type]

# Settings
league_id = '416585'

# Pull FPL data
league_data = requests.get(f'https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/').json()
fpl_data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
e = next(event for event in fpl_data['events'] if event['is_current'])
gw = e['id']
weekly_stats = {}
gw_data = {}
weekly_picks = {}
for manager in league_data['standings']['results']:
    id = manager['entry']
    weekly_stats[id] = requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/history/').json()
    gw_data[id] = requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{gw}/picks/').json()
    weekly_picks[id] = {i: requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{i}/picks/').json()['picks'] for i in range(1,gw+1)}

# Setup datasets
team_name, total_points, rank, rank_chg, value_gain, green_streaks, pos_total_points = {}, {}, {}, {}, {}, {}, {pos: {} for pos in ['GK','DEF','MID','FWD']}
for manager in league_data['standings']['results']:
    id = manager['entry']
    team_name[id] = manager['entry_name']
    total_points[id] = manager['total']
    rank[id] = manager['rank']
    rank_chg[id] = manager['last_rank'] - manager['rank']
    value_gain[id] = (weekly_stats[id]['current'][-1]['value'] - weekly_stats[id]['current'][-2]['value']) / 10
    for pos in pos_total_points:
        pos_total_points[pos][id] = 0

all_gws_players_stats = {i: {player['id']: player['stats'] for player in requests.get(f'https://fantasy.premierleague.com/api/event/{i}/live/').json()['elements']} for i in range(1,gw+1)}
players_stats = {element['id']: element for element in fpl_data['elements']}
selected = {key: 0 for key in all_gws_players_stats[gw].keys()}
captained = {key: 0 for key in all_gws_players_stats[gw].keys()}

gw_points, team_value, hits, bench_pts, best_captained, captains, transfers_gain, subs_pts, itb, correct_gk = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
chips = {chip: [] for chip in ['bboost', 'freehit', 'wildcard', '3xc']}

for id in gw_data:
    gw_points[id] = gw_data[id]['entry_history']['points']
    team_value[id] = gw_data[id]['entry_history']['value'] / 10
    if gw_data[id]['entry_history']['event_transfers_cost'] > 0:
         hits[id] = gw_data[id]['entry_history']['event_transfers_cost']
    if gw_data[id]['entry_history']['points_on_bench'] != 0:
        bench_pts[id] = gw_data[id]['entry_history']['points_on_bench']
    itb[id] = gw_data[id]['entry_history']['bank'] / 10
    if gw_data[id]['active_chip'] is not None:
        chips[gw_data[id]['active_chip']].append(id)
    for p in gw_data[id]['picks']:
        selected[p['element']] += 1
        if p['is_captain'] is True:
            captained[p['element']] += 1
        if p['multiplier'] > 1:
            captains[id] = p['element']
            best_captained[id] = players_stats[p['element']]['event_points'] * p['multiplier']
    for i in range(gw-1,0,-1):
        if weekly_stats[id]['current'][i]['overall_rank'] < weekly_stats[id]['current'][i-1]['overall_rank']:
            green_streaks[id] = green_streaks[id] + 1 if id in green_streaks.keys() else 1
        else:
            break
    if gw_data[id]['entry_history']['event_transfers'] > 0:
            this_picks = [player['element'] for player in gw_data[id]['picks']]
            prev_json = requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{gw-1}/picks/').json()
            if prev_json['active_chip'] != 'freehit':
                last_picks = [player['element'] for player in prev_json['picks']]
            else:
                last_picks = [player['element'] for player in requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{gw-2}/picks/').json()['picks']]
            transfers_gain[id] = sum(players_stats[value]['event_points'] for value in list(set(this_picks) - set(last_picks))) - sum(players_stats[value]['event_points'] for value in list(set(last_picks) - set(this_picks))) - gw_data[id]['entry_history']['event_transfers_cost']
    if len(gw_data[id]['automatic_subs']) > 0:
        subs_pts[id] = sum(players_stats[value]['event_points'] for value in [sub['element_in'] for sub in gw_data[id]['automatic_subs']])
    gk_count = 0
    for week in range(1,gw+1):
        if all_gws_players_stats[week][weekly_picks[id][week][0]['element']]['total_points'] >= all_gws_players_stats[week][weekly_picks[id][week][11]['element']]['total_points']:
            gk_count += 1
        for pick in weekly_picks[id][week]:
            if pick['multiplier'] > 0:
                pos_total_points[element_type_to_pos(players_stats[pick['element']]['element_type'])][id] += all_gws_players_stats[week][pick['element']]['total_points']*pick['multiplier']
    correct_gk[id] = (gk_count/gw)*100
        
# Prepare data for summary
max_gw_pts = [key for key, value in gw_points.items() if value == max(gw_points.values())]
max_team_value = [key for key, value in team_value.items() if value == max(team_value.values())]
min_team_value = [key for key, value in team_value.items() if value == min(team_value.values())]
max_selected = [key for key, value in selected.items() if value == max(selected.values())]
max_captain = [key for key, value in captained.items() if value == max(captained.values())]
max_hits = [key for key, value in hits.items() if value == max(hits.values())]
max_bench_pts = [key for key, value in bench_pts.items() if value == max(bench_pts.values())]
max_greens = [key for key, value in green_streaks.items() if value == max(green_streaks.values())]
max_transfers_gain = [key for key, value in transfers_gain.items() if value == max(transfers_gain.values())]
max_subs_pts = [key for key, value in subs_pts.items() if value == max(subs_pts.values())]
max_itb = [key for key, value in itb.items() if value == max(itb.values())]
max_correct_gk = [key for key, value in correct_gk.items() if value == max(correct_gk.values())]
pts_by_positions = [(pos, [key for key, value in pos_total_points[pos].items() if value == max(pos_total_points[pos].values())]) for pos in ['GK','DEF','MID','FWD']]
max_bst_cptn = [key for key, value in best_captained.items() if value == max(best_captained.values())]
bst_cptn_ids = list(set([captains[id] for id in max_bst_cptn]))

league_summary = ""
league_summary += f"** {league_data['league']['name']} GW {gw}:\n"
league_summary += "Standings: " + ' '.join([f"({item['rank']}) {get_team_name(item['entry'])}" for item in league_data['standings']['results'][0:3]]) + "\n------------------------------\n"
if max(gw_points.values()) > 0:
    league_summary += "Most Points: " + ' & '.join(list(map(get_team_name, max_gw_pts))) + " (" + str(gw_points[max(gw_points, key=gw_points.get)]) + " Points, Overall GW Rank: " + format(gw_data[max(gw_points, key=gw_points.get)]['entry_history']['rank'],',d') + ")\n"
league_summary += "Most Selected: " + ' & '.join(list(map(get_player_webname, max_selected))) + " (" + str(selected[max(selected, key=selected.get)]) + " Teams)" + "\n"
league_summary += "Captained Best: " + ' & '.join(list(map(get_team_name, max_bst_cptn))) + " (" + ' & '.join(list(map(get_player_webname, bst_cptn_ids))) + ", " + str(max(best_captained.values())) + " Points)" + "\n"
league_summary += "Most Captained: " + ' & '.join(list(map(get_player_webname, max_captain))) + " (" + str(captained[max(captained, key=captained.get)]) + " Teams)" + "\n------------------------------\n"
league_summary += "Highest Team Value: " + ' & '.join(list(map(get_team_name, max_team_value))) + " (" + str(team_value[max(team_value, key=team_value.get)]) + "M £)" + "\n"
league_summary += "Lowest Team Value: " + ' & '.join(list(map(get_team_name, min_team_value))) + " (" + str(team_value[min(team_value, key=team_value.get)]) + "M £)" + "\n"
league_summary += "Going Up: " + ' & '.join(list(map(get_team_name, max_greens))) + " (" + str(green_streaks[max(green_streaks, key=green_streaks.get)]) + " Greens)" + "\n"
league_summary += "Highest Money in the Bank: " + ' & '.join(list(map(get_team_name, max_itb))) + " (" + str(itb[max(itb, key=itb.get)]) + "M £)" + "\n"
if len(max_hits) > 0:
    league_summary += "Most Hits: " + ' & '.join(list(map(get_team_name, max_hits))) + " (-" + str(hits[max(hits, key=hits.get)]) + " Points" + ")\n------------------------------\n"
else:
    league_summary += "Most Hits: None\n------------------------------\n"
if len(max_subs_pts) > 0:
    league_summary += "Highest Substitutes Points: " + ' & '.join(list(map(get_team_name, max_subs_pts))) + " (" + str(subs_pts[max(subs_pts, key=subs_pts.get)]) + " Points)" + "\n"
if max(bench_pts.values()) > 0:
    league_summary += "Most Points on Bench: " + ' & '.join(list(map(get_team_name, max_bench_pts))) + " (" + str(bench_pts[max(bench_pts, key=bench_pts.get)]) + " Points" + ")\n"
if len(max_transfers_gain) > 0:
    league_summary += "Highest Transfers Gain: " + ' & '.join(list(map(get_team_name, max_transfers_gain))) + " (" + str(transfers_gain[max(transfers_gain, key=transfers_gain.get)]) + " Points)" + "\n"
league_summary += "Correct GK: " + ' & '.join(list(map(get_team_name, max_correct_gk))) + " (" + str(round(correct_gk[max(correct_gk, key=correct_gk.get)],2)) + "%)" + "\n------------------------------\n"
for chip in chips:
    if len(chips[chip]) > 0:
        league_summary += f"{get_chip_name(chip)} Used: " + ' & '.join(list(map(get_team_name, chips[chip]))) + "\n"
league_summary += "------------------------------\n"
league_summary += "".join(f"Most {pos} Points: " + ' & '.join(list(map(get_team_name, max_points))) + f" ({str(pos_total_points[pos][max(pos_total_points[pos], key=pos_total_points[pos].get)])} Points)\n" for pos, max_points in pts_by_positions)
print(league_summary)

# Graphics
dict_list = [total_points, gw_points, team_value, hits, bench_pts, best_captained, green_streaks, transfers_gain, subs_pts, itb, correct_gk, pos_total_points['GK'], pos_total_points['DEF'], pos_total_points['MID'], pos_total_points['FWD']]
dict_list_sorted = [dict(sorted(d.items(), key=lambda item: item[1], reverse=False)) for d in dict_list]
dict_list_sorted[0] = {key: total_points[key] for key in sorted(rank, key=lambda x: (rank[x], x), reverse=True)}
titles = [
    "Total Points", "Gameweek Points", "Team Value", "Hits Taken", "Bench Points", 
    "Captain Points", "Green Streaks", "Transfers Gain", "Substitution Points", "In The Bank", 
    "Correct Goalkeeper", "Goalkeeper Total Points", "Defender Total Points", "Midfielder Total Points", "Forward Total Points"
]
# Total Points
tp_lower = math.ceil((min(total_points.values())-200) / 100) * 100
# Team Value
tv_lower = math.ceil(min(team_value.values())-4)
# Position Points
gk_lower = math.ceil((min(pos_total_points['GK'].values())-10) / 10) * 10
def_lower = math.ceil((min(pos_total_points['DEF'].values())-10) / 10) * 10
mid_lower = math.ceil((min(pos_total_points['MID'].values())-10) / 10) * 10
fwd_lower = math.ceil((min(pos_total_points['FWD'].values())-10) / 10) * 10
fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(22, 13.2))
axes = axes.flatten()
for i, (ax, data_dict) in enumerate(zip(axes, dict_list_sorted)):
    if not data_dict:
        ax.set_title(titles[i])
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        continue
    keys = [get_team_name(key) for key in data_dict.keys()]
    values = list(data_dict.values())
    colors = ['skyblue' for key in data_dict.keys()]
    bars = ax.barh(keys, values, color=colors)  
    ax.set_title(titles[i])
    max_value = max(values)
    min_value = min(values)
    label_length_factor = 0.02
    for bar in bars:
        width = bar.get_width()
        if width != 0:
            if i+1==1:
                key_id = list(data_dict.keys())[bars.index(bar)]
                player_rank = rank.get(key_id, 0)
                player_chg = rank_chg.get(key_id, 0)
                bar_label = f'Rank: {player_rank} (+{player_chg})' if player_chg > 0 else f'Rank: {player_rank} ({player_chg})' if player_chg != 0 else f'Rank: {player_rank}'
                ax.text(tp_lower/2+width/2, bar.get_y() + bar.get_height()/2, bar_label, 
                        va='center', ha='center' if width > 0 else 'right', color='black', fontsize=10) 
                ax.text(width, bar.get_y() + bar.get_height()/2, f'{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10) 
            elif i+1==3:
                key_id = list(data_dict.keys())[bars.index(bar)]
                value = team_value.get(key_id, 0)
                value_change = value_gain.get(key_id, 0)
                bar_value = f'{value} (+{value_change})' if value_change > 0 else f'{value} ({value_change})' if value_change != 0 else f'{value}'
                ax.text(tv_lower/2+width/2, bar.get_y() + bar.get_height()/2, bar_value, 
                        va='center', ha='center' if width > 0 else 'right', color='black', fontsize=10) 
            elif i+1==4:
                ax.text(width, bar.get_y() + bar.get_height()/2, f'-{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10)
            elif i+1==11:
                ax.text(width/2, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
                    va='center', ha='center' if width > 0 else 'right', color='black', fontsize=10)
            else:
                ax.text(width, bar.get_y() + bar.get_height()/2, f'{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10) 
        else:
            if min_value < 0:
                ax.text(width, bar.get_y() + bar.get_height()/2, f'{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10) 
    if i+1==4:
        x_ticks = ax.get_xticks()
        ax.set_xticklabels([f'-{int(tick)}' if tick != 0 else '0' for tick in x_ticks])
    if i+1 in [5,6,7,8,9]:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if i+1==1:
        buffer = (max_value-tp_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-tp_lower)
        ax.set_xlim(tp_lower, max_value+buffer)
    elif i+1==3:
        ax.set_xlim(tv_lower, 0.05*(max_value-min_value) + max_value)
    elif i+1 in [5,6,8]:
        max_buffer = (max_value-min_value) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-min_value)
        min_buffer = (min_value-max_value) * 0.05 + label_length_factor * len(str(min_value)) * (min_value-max_value)
        if min_value < 0:
            ax.set_xlim(min_value+min_buffer, max_value+max_buffer)
        else:
            ax.set_xlim(0, max_value+max_buffer)
    elif i+1==9:
        if min_value < 0:
            max_buffer = (max_value-min_value) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-min_value)
            min_buffer = (min_value-max_value) * 0.05 + label_length_factor * len(str(min_value)) * (min_value-max_value)
            ax.set_xlim(min_value+min_buffer, max_value+max_buffer)
        else:
            buffer = max_value * 0.05 + label_length_factor * len(str(max_value)) * max_value
            ax.set_xlim(0, max_value + buffer)
    elif i+1==11:
        ax.set_xlim(0, 105)
        ax.set_xticks([0, 20, 40, 60, 80, 100])
        ax.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
    elif i+1==12:
        buffer = (max_value-gk_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-gk_lower)
        ax.set_xlim(gk_lower, max_value+buffer)
    elif i+1==13:
        buffer = (max_value-def_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-def_lower)
        ax.set_xlim(def_lower, max_value+buffer)
    elif i+1==14:
        buffer = (max_value-mid_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-mid_lower)
        ax.set_xlim(mid_lower, max_value+buffer)
    elif i+1==15:
        buffer = (max_value-fwd_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-fwd_lower)
        ax.set_xlim(fwd_lower, max_value+buffer)
    else:
        buffer = max_value * 0.05 + label_length_factor * len(str(max_value)) * max_value
        ax.set_xlim(0, max_value + buffer)
for j in range(len(dict_list_sorted), len(axes)):
    fig.delaxes(axes[j])
plt.suptitle(f"{league_data['league']['name']} - Gameweek {gw}", fontsize=24)
plt.tight_layout()
plt.savefig(f"GW{gw}.png", format="png", bbox_inches="tight")
