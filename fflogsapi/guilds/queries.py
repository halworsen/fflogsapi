# Query to retrieve information about a guild
Q_GUILD = '''
query {{
    guildData {{
        guild({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Query to retrieve paginated guilds from the entire site
Q_GUILD_PAGINATION = '''
query {{
    guildData {{
        guilds({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Top level query for retrieving paginated attendance reports
Q_GUILD_ATTENDANCE_PAGINATION = '''
query {{
    guildData {{
        guild(id: {guildID}) {{
            attendance({filters}) {{
                {innerQuery}
            }}
        }}
    }}
}}
'''

# Query to retrieve paginated guild member character data
Q_GUILD_CHARACTER_PAGINATION = '''
query {{
    guildData {{
        guild(id: {guildID}) {{
            members({filters}) {{
                {innerQuery}
            }}
        }}
    }}
}}
'''

# Inner query to retrieve ranking information for a guild
Q_GUILD_RANKING = '''
zoneRanking(zoneId: {zoneID}) {{
    completeRaidSpeed(size: {size}, difficulty: {difficulty}) {{
        worldRank {{ number, color }},
        regionRank {{ number, color }},
        serverRank {{ number, color }},
    }},
    progress(size: {size}) {{
        worldRank {{ number, color }},
        regionRank {{ number, color }},
        serverRank {{ number, color }},
    }},
    speed(size: {size}, difficulty: {difficulty}) {{
        worldRank {{ number, color }},
        regionRank {{ number, color }},
        serverRank {{ number, color }},
    }},
}}
'''
