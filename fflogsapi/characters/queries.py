# Retrieves character data
Q_CHARACTER_DATA = '''
query {{
    characterData {{
        character({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''
