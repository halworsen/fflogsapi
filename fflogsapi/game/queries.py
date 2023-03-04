# Query to retrieve information about an ability
Q_ABILITY = '''
query {{
    gameData {{
        ability(id: {abilityID}) {{
            name,
            description,
            icon,
        }}
    }}
}}
'''

# Query to retrieve a page of game abilities
Q_ABILITY_PAGINATION = '''
query {{
    gameData {{
        abilities({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Query to retrieve information about all supported jobs
# Classes aren't supported by FF Logs, only specs (jobs)
Q_JOBS = '''
query {
    gameData {
        class(id: 1) {
            specs {
                id,
                name,
                slug,
            }
        }
    }
}
'''

# Query to retrieve information about an item
Q_ITEM = '''
query {{
    gameData {{
        item(id: {itemID}) {{
            name,
            icon,
        }}
    }}
}}
'''

# Query to retrieve a page of game items
Q_ITEM_PAGINATION = '''
query {{
    gameData {{
        items({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Query to retrieve information about a map
Q_MAP = '''
query {{
    gameData {{
        map(id: {mapID}) {{
            name,
            filename,
            offsetX,
            offsetY,
            sizeFactor,
        }}
    }}
}}
'''

# Query to retrieve a page of game maps
Q_MAP_PAGINATION = '''
query {{
    gameData {{
        maps({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Query to retrieve information about all grand companies
Q_GRAND_COMPANIES = '''
query {
    gameData {
        factions {
            id,
            name,
        }
    }
}
'''
