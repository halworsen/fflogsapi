import matplotlib.pyplot as plt
from fflogsapi.client import FFLogsClient
from fflogsapi.data import Report, Fight
from fflogsapi.queries import *
from datetime import datetime
import pickle
import os
import numpy as np

from config import *

def main():
    fapi = FFLogsClient(CLIENT_ID, CLIENT_SECRET)

    reports = None
    if LOAD_SAVED_DATA and os.path.exists('./data.pkl'):
        with open('data.pkl', 'rb') as f:
            reports = pickle.load(f)
    else:
        reports = fapi.get_all_reports(GUILD_ID)
        with open('data.pkl', 'wb+') as f:
            pickle.dump(reports, f)

    reports = sorted(reports, key=lambda r: r.start)

    time_spent_raiding = []
    time_per_boss = {boss: [] for boss in INTERESTING_FIGHTS}
    raid_days = []
    wipes_per_boss = {boss: [] for boss in INTERESTING_FIGHTS}
    wipes_before_clear = {boss: [] for boss in INTERESTING_FIGHTS}
    min_percentages = {boss: [] for boss in INTERESTING_FIGHTS}
    clears = {}

    cum_hours = 0
    for report in reports:
        start = datetime.fromtimestamp(report.start * TIMESTAMP_PRECISION)
        end = datetime.fromtimestamp(report.end * TIMESTAMP_PRECISION)
        cum_hours += (report.duration() * TIMESTAMP_PRECISION) / 3600
        if start < START_DATE:
            continue
    
        time_spent_raiding.append(cum_hours)
        raid_days.append(start)

        boss_times = {boss: 0 for boss in INTERESTING_FIGHTS}
        boss_wipes = {boss: 0 for boss in INTERESTING_FIGHTS}
        boss_wipes_before_clear = {boss: 0 for boss in INTERESTING_FIGHTS}
        day_min_percentages = {boss: 100 for boss in INTERESTING_FIGHTS}
        for fight in report:
            boss = fight.name
            if fight.difficulty and fight.difficulty < MINIMUM_DIFFICULTY:
                continue
            if boss not in INTERESTING_FIGHTS:
                continue

            # Record clear dates
            if fight.kill and boss not in clears:
                clears[boss] = start
            elif fight.kill == False:
                boss_wipes[boss] += 1
                if boss not in clears:
                    boss_wipes_before_clear[boss] += 1
            
            # Record time spent per boss on each day
            boss_times[boss] += (fight.duration() * TIMESTAMP_PRECISION) / 3600

            # Record minimum boss health reached (as a percentage)
            if fight.fightPercentage:
                day_min_percentages[boss] = min(day_min_percentages[boss], fight.fightPercentage)

        for boss in INTERESTING_FIGHTS:
            prev_boss_time_cum = time_per_boss[boss][-1] if len(time_per_boss[boss]) else 0
            prev_wipes_cum = wipes_per_boss[boss][-1] if len(wipes_per_boss[boss]) else 0
            prev_wipes_before_clear_cum = wipes_before_clear[boss][-1] if len(wipes_before_clear[boss]) else 0
            prev_day_min_percentages = min_percentages[boss][-1] if len(min_percentages[boss]) else 100

            time_per_boss[boss].append(prev_boss_time_cum + boss_times[boss])
            wipes_per_boss[boss].append(prev_wipes_cum + boss_wipes[boss])
            wipes_before_clear[boss].append(prev_wipes_before_clear_cum + boss_wipes_before_clear[boss])
            min_percentages[boss].append(min(prev_day_min_percentages, day_min_percentages[boss]))
    

    # Trim away bosses that haven't been cleared yet from the "wipes before clear" metric
    to_remove = []
    for boss in wipes_before_clear.keys():
        if boss not in clears:
            to_remove.append(boss)
    for boss in to_remove:
        wipes_before_clear.pop(boss)

    if not os.path.exists('./figures'):
        os.makedirs('./figures')

    plt.figure()
    plt.title('Hours spent raiding')
    plt.plot(raid_days, time_spent_raiding)
    for boss, clear_date in clears.items():
        plt.axvline(clear_date, ymin=0, ymax=cum_hours, color=BOSS_COLORS[boss])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./figures/hours_spent.png')

    plt.figure()
    plt.title('Hours spent in fight per boss')
    for boss, times in time_per_boss.items():
        plt.plot(raid_days, times, color=BOSS_COLORS[boss])
    plt.legend(time_per_boss.keys())
    for boss, clear_date in clears.items():
        plt.axvline(clear_date, ymin=0, ymax=cum_hours, color=BOSS_COLORS[boss])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./figures/hours_per_boss.png')

    plt.figure()
    plt.title('Minimum percentage reached per boss')
    for boss, percentages in min_percentages.items():
        plt.plot(raid_days, percentages, color=BOSS_COLORS[boss])
    plt.legend(min_percentages.keys())
    for boss, clear_date in clears.items():
        plt.axvline(clear_date, ymin=0, ymax=cum_hours, color=BOSS_COLORS[boss])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./figures/min_percent.png')

    plt.figure()
    plt.title('Wipes per boss')
    for boss, wipes in wipes_per_boss.items():
        plt.plot(raid_days, wipes, color=BOSS_COLORS[boss])
    for boss, clear_date in clears.items():
        plt.axvline(clear_date, ymin=0, ymax=cum_hours, color=BOSS_COLORS[boss])
    plt.legend(wipes_per_boss.keys())
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./figures/wipes_per_boss.png')

    plt.figure()
    plt.title('Total wipes per boss')
    wipes_total = [wipes[-1] for wipes in wipes_per_boss.values()]
    plt.bar(wipes_per_boss.keys(), wipes_total, color=BOSS_COLORS.values())
    plt.tight_layout()
    plt.savefig('./figures/bar_wipes_per_boss.png')

    plt.figure()
    plt.title('Total wipes before clear')
    wipes_total = [wipes[-1] for wipes in wipes_before_clear.values()]
    plt.bar(wipes_before_clear.keys(), wipes_total, color=BOSS_COLORS.values())
    plt.tight_layout()
    plt.savefig('./figures/wipes_before_clear.png')

    # Needs to use wipes_before_clears as keys. It doesn't make sense to compute reclear wipes on bosses that aren't cleared yet
    plt.figure()
    plt.title('Total wipes during reclears')
    reclear_wipes = [wipes_per_boss[boss][-1] - wipes_before_clear[boss][-1] for boss in wipes_before_clear.keys()]
    plt.bar(wipes_before_clear.keys(), reclear_wipes, color=BOSS_COLORS.values())
    plt.tight_layout()
    plt.savefig('./figures/reclear_wipes.png')

    print('THE NUMBERS (what do they mean)\n================================')
    print(f'Hours until clear:')
    for boss, clear_date in clears.items():


if __name__ == '__main__':
    main()
