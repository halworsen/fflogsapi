# Top level query for retrieving paginated characters
Q_CHARACTER_PAGINATION = """
query {{
    characterData {{
        characters({filters}) {{
            {innerQuery}
        }}
    }}
}}
"""

# Retrieves character data
Q_CHARACTER_DATA = """
query {{
    characterData {{
        character({filters}) {{
            {innerQuery}
        }}
    }}
}}
"""
