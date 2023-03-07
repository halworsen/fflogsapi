# Retrieve information about a specific encounter
Q_ENCOUNTER = '''
query {{
    worldData {{
        encounter(id: {encounterID}) {{
            {innerQuery}
        }}
    }}
}}
'''
# Retrieve information about a specific expansion
Q_EXPANSION = '''
query {{
    worldData {{
        expansion(id: {expansionID}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve information about all supported expansions
Q_EXPANSION_LIST = '''
query {{
    worldData {{
        expansions {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve information about a specific region
Q_REGION = '''
query {{
    worldData {{
        region(id: {regionID}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve information about all supported regions
Q_REGION_LIST = '''
query {{
    worldData {{
        regions {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve a pagination of servers belonging to a region
Q_REGION_SERVER_PAGINATION = '''
query {{
    worldData {{
        region(id: {regionID}) {{
            servers({filters}) {{
                {innerQuery}
            }}
        }}
    }}
}}
'''

# Retrieve a pagination of servers belonging to a subregion
Q_SUBREGION_SERVER_PAGINATION = '''
query {{
    worldData {{
        subregion(id: {subregionID}) {{
            servers({filters}) {{
                {innerQuery}
            }}
        }}
    }}
}}
'''

# Retrieve information about a server, either by ID or slug+region
Q_SERVER = '''
query {{
    worldData {{
        server({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve a pagination of characters belonging to a server
Q_SERVER_CHARACTER_PAGINATION = '''
query {{
    worldData {{
        server(id: {serverID}) {{
            characters({filters}) {{
                {innerQuery}
            }}
        }}
    }}
}}
'''

# Retrieve information about a given subregion
Q_SUBREGION = '''
query {{
    worldData {{
        subregion(id: {subregionID}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve information about a given zone
Q_ZONE = '''
query {{
    worldData {{
        zone(id: {zoneID}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve information about all zones, filterable by expansion ID
Q_ZONE_LIST = '''
query {{
    worldData {{
        zones({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''
