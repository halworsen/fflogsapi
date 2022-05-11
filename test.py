from typing import Dict
from config import *
from fflogsapi.client import FFLogsClient
from fflogsapi.constants import *

def metric_hours_spent(client: FFLogsClient) -> int:
    total_time = 0

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            total_time += report.duration()
    
    return (total_time * 1e-3) / 3600

def metric_hours_per_boss(client: FFLogsClient) -> Dict[str, int]:
    hours = {}

    reports = []
    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            reports.append(report)

    reports = sorted(reports, key=lambda r: r.get_start_time())
    for report in reports:
        for fight in report:
            difficulty = fight.get_difficulty() 
            if difficulty and difficulty < FIGHT_DIFFICULTY_SAVAGE:
                continue

            name = fight.name()
            if name not in hours:
                hours[name] = 0
            hours[name] += (fight.duration() * 1e-3) / 3600

    return hours

def metric_hours_to_clear(client: FFLogsClient) -> Dict[str, int]:
    hours = {}
    cleared_bosses = []

    reports = []
    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            reports.append(report)

    reports = sorted(reports, key=lambda r: r.get_start_time())
    for report in reports:
        for fight in report:
            difficulty = fight.get_difficulty() 
            if difficulty and difficulty < FIGHT_DIFFICULTY_SAVAGE:
                continue

            name = fight.name()
            if name in cleared_bosses:
                continue
            if name not in hours:
                hours[name] = 0
            hours[name] += (fight.duration() * 1e-3) / 3600

            if fight.is_kill():
                cleared_bosses.append(name)

    return hours

def metric_deaths(client: FFLogsClient) -> int:
    deaths = {'total': 0, 'covid': 0, 'wall': 0}

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            report._get_master_data()

            for fight in report:
                table = fight.get_fight_table()
                if not table:
                    continue
                if 'deathEvents' not in table:
                    continue

                deaths['total'] += len(table['deathEvents'])
                for death in table['deathEvents']:
                    if death['name'] not in deaths:
                        deaths[death['name']] = 0
                    deaths[death['name']] += 1

                    if 'ability' in death and death['ability']['name'] == 'Cursed Casting':
                        deaths['covid'] += 1
                    elif 'ability' not in death:
                        deaths['wall'] += 1

    return deaths

def metric_nemeses(client: FFLogsClient) -> int:
    deaths = {}

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            report._get_master_data()

            for fight in report:
                table = fight.get_fight_table()
                if not table:
                    continue
                if 'deathEvents' not in table:
                    continue

                for death in table['deathEvents']:
                    if death['name'] not in deaths:
                        deaths[death['name']] = {}
                    
                    if 'ability' not in death:
                        continue
                    
                    if death['ability']['name'] not in deaths[death['name']]:
                        deaths[death['name']][death['ability']['name']] = 0

                    deaths[death['name']][death['ability']['name']] += 1
    
    nemeses = {}
    for player, causes in deaths.items():
        nemesis = ''
        nemesis_deaths = 0
        for cause, count in causes.items():
            if 'attack' in cause:
                continue
            if count > nemesis_deaths:
                nemesis = cause
                nemesis_deaths = count
        nemeses[player] = (nemesis, nemesis_deaths)

    return nemeses

def metric_action_use(client: FFLogsClient) -> int:
    cool_abilities = {
        'rez': {'total': 0},
        'invuln': {'total': 0},
        'dragon_kick': 0,
        'dosis': 0,
        'celestial': 0,
        'divination': 0,
    }

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            report._get_master_data()

            actors = report.get_actors()
            actor_map = {}
            for actor in actors:
                actor_map[actor.id] = actor

            abilities = report.get_abilities()
            ability_map = {}
            for ability in abilities:
                ability_map[ability.game_id] = ability

            rezzes = ['Egeiro', 'Ascend', 'Resurrection']
            rez_ids = [a.game_id for a in abilities if a.name in rezzes]

            invulns = ['Holmgang', 'Superbolide']
            invuln_ids = [a.game_id for a in abilities if a.name in invulns]

            dragon_kick_id = [a.game_id for a in abilities if a.name == 'Dragon Kick']
            dosis_id = [a.game_id for a in abilities if a.name == 'Dosis III']
            divination_id = [a.game_id for a in abilities if a.name == 'Divination']
            celestial_id = [a.game_id for a in abilities if a.name == 'Celestial Oppossition']

            for fight in report:
                events = fight.get_fight_events()
                if events is None:
                    continue

                for event in events:
                    if 'sourceID' not in event:
                        continue

                    if 'abilityGameID' not in event:
                        continue
                    ability = ability_map[event['abilityGameID']]

                    if ability.game_id in rez_ids:
                        if ability.name not in cool_abilities['rez']:
                            cool_abilities['rez'][ability.name] = 0
                        cool_abilities['rez'][ability.name] += 1
                        cool_abilities['rez']['total'] += 1
                    
                    if ability.game_id in invuln_ids:
                        if ability.name not in cool_abilities['invuln']:
                            cool_abilities['invuln'][ability.name] = 0
                        cool_abilities['invuln'][ability.name] += 1
                        cool_abilities['invuln']['total'] += 1
                    
                    if ability.game_id in dragon_kick_id:
                        cool_abilities['dragon_kick'] += 1

                    if ability.game_id in dosis_id:
                        cool_abilities['dosis'] += 1
                    
                    if ability.game_id in celestial_id:
                        cool_abilities['celestial'] += 1

                    if ability.game_id in divination_id:
                        cool_abilities['divination'] += 1

    return cool_abilities

def metric_consumable_usage(client: FFLogsClient) -> int:
    pot_uses = {'total': 0}

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            report._get_master_data()

            actors = report.get_actors()
            actor_map = {}
            for actor in actors:
                actor_map[actor.id] = actor
            abilities = report.get_abilities()
            # find medication abilities
            medication = list(filter(lambda a: a.name == 'Medicated', abilities))
            medication_ids = [a.game_id for a in medication]

            for fight in report:
                events = fight.get_fight_events()
                if events is None:
                    continue

                for event in events:
                    if 'sourceID' not in event:
                        continue

                    if event['type'] == EVENT_TYPE_COMBATANT_INFO:
                        actor = actor_map[event['sourceID']]
                        if actor.type != 'Player':
                            continue
                        auras = event['auras']
                        for aura in auras:
                            if aura['ability'] in medication_ids:
                                pot_uses['total'] += 1

                                if actor.name not in pot_uses:
                                    pot_uses[actor.name] = 0
                                pot_uses[actor.name] += 1
                    if event['type'] == EVENT_TYPE_APPLY_BUFF:
                        actor = actor_map[event['sourceID']]
                        target = actor_map[event['targetID']]
                        if target.type != 'Player':
                            continue
                        if actor.type != 'Player':
                            continue
                        if event['abilityGameID'] in medication_ids:
                            pot_uses['total'] += 1
                            if actor.name not in pot_uses:
                                pot_uses[actor.name] = 0
                            pot_uses[actor.name] += 1

    return pot_uses

def metric_biggest_damage(client: FFLogsClient) -> int:
    damage = {
        'biggest_single': {'player': None, 'ability': None, 'target': None, 'damage': 0},
        'most_in_fight': {'player': None, 'damage': 0},
        'bahamut': 0,
    }

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            report._get_master_data()

            actors = report.get_actors()
            actor_map = {}
            for actor in actors:
                actor_map[actor.id] = actor

            abilities = report.get_abilities()
            ability_map = {}
            for ability in abilities:
                ability_map[ability.game_id] = ability

            for fight in report:
                events = fight.get_fight_events()
                table = fight.get_fight_table()

                difficulty = fight.get_difficulty()
                if not difficulty or difficulty < FIGHT_DIFFICULTY_SAVAGE:
                    continue

                if fight.name() not in ['Erichthonios', 'Phoinix', 'Hippokampos', 'Hesperos']:
                    continue

                if events:
                    for event in events:
                        if event['type'] != EVENT_TYPE_DAMAGE and event['type'] != EVENT_TYPE_CALCULATED_DAMAGE:
                            continue

                        source = actor_map[event['sourceID']]
                        target = actor_map[event['targetID']]
                        if source.type not in  ['Player', 'Pet']:
                            continue

                        if target.type == 'Player':
                            continue

                        if source.name == 'Limit Break':
                            continue
                        
                        if source.name in ['Cake Mix', 'Ras Avasch']:
                            continue
                        
                        if source.name == 'Demi-Bahamut':
                            damage['bahamut'] += event['amount']

                        if event['amount'] > damage['biggest_single']['damage']:
                            damage['biggest_single'] = {
                                'player': source,
                                'target': target,
                                'ability': ability_map[event['abilityGameID']],
                                'damage': event['amount'],
                                'report': report.title(),
                            }

                if table:
                    for player in table['damageDone']:
                        if player['total'] > damage['most_in_fight']['damage']:
                            damage['most_in_fight'] = {
                                'player': actor_map[player['id']],
                                'damage': player['total'],
                                'fight': fight.name(),
                                'report': report.title(),
                            }

    return damage

def metric_healing(client: FFLogsClient) -> int:
    heals = {
        'biggest_single': {'player': None, 'ability': None, 'target': None, 'heal': 0},
        'total': 0,
        'overheal': 0,
    }

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            report._get_master_data()

            actors = report.get_actors()
            actor_map = {}
            for actor in actors:
                actor_map[actor.id] = actor

            abilities = report.get_abilities()
            ability_map = {}
            for ability in abilities:
                ability_map[ability.game_id] = ability

            for fight in report:
                events = fight.get_fight_events()

                difficulty = fight.get_difficulty()
                if not difficulty or difficulty < FIGHT_DIFFICULTY_SAVAGE:
                    continue

                if fight.name() not in ['Erichthonios', 'Phoinix', 'Hippokampos', 'Hesperos']:
                    continue

                if not events:
                    continue

                for event in events:
                    if event['type'] != EVENT_TYPE_HEAL:
                        continue

                    source = actor_map[event['sourceID']]
                    target = actor_map[event['targetID']]

                    if source.type != 'Player':
                        continue

                    if source.type != 'Player':
                        continue
                    
                    heals['total'] += event['amount']
                    if 'overheal' in event:
                        heals['overheal'] += event['overheal']
                    if event['amount'] > heals['biggest_single']['heal']:
                        heals['biggest_single'] = {
                            'player': source,
                            'target': target,
                            'ability': ability_map[event['abilityGameID']],
                            'heal': event['amount'],
                            'report': report.title(),
                        }

    return heals

def metric_cinderwings(client: FFLogsClient) -> int:
    cinderwings = 0

    for page in client.pages({ 'guildID': 100658 }):
        for report in page:
            report.fetch_batch()
            report._get_master_data()

            abilities = report.get_abilities()
            ability_map = {}
            for ability in abilities:
                ability_map[ability.game_id] = ability

            for fight in report:
                events = fight.get_fight_events()
                if events:
                    for event in events:
                        if 'abilityGameID' not in event:
                            continue
                        
                        ability = ability_map[event['abilityGameID']]
                        if 'Cinderwing' in ability.name:
                            cinderwings += 1

    return cinderwings

if __name__ == '__main__':
    fapi = FFLogsClient(CLIENT_ID, CLIENT_SECRET, ignore_cache_expiry=True)

    try:
        print('Hours spent raiding:', metric_hours_spent(fapi))
        print('Hours per boss:', metric_hours_per_boss(fapi))
        print('Hours to clear each boss:', metric_hours_to_clear(fapi))
        print('Total deaths:', metric_deaths(fapi))
        print('Nemeses:', metric_nemeses(fapi))
        print('Action usage:', metric_action_use(fapi))
        print('Potions used:', metric_consumable_usage(fapi))
        print('Biggest damage:', metric_biggest_damage(fapi))
        print('Total heal:', metric_healing(fapi))
        print('Cinderwings eaten:', metric_cinderwings(fapi))
    except KeyboardInterrupt as e:
        print(e)
        pass

    print('saving cache')
    #fapi.save_cache()
