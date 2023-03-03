# Query to retrieve information about a current prog race
Q_PROG_RACE = '''
query {{
    progressRaceData {{
        {innerQuery}
    }}
}}
'''
