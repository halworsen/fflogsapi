# Top level query for retrieving paginated reports
Q_REPORT_PAGINATION = """
query {{
    reportData {{
        reports({filters}) {{
            {innerQuery}
        }}
    }}
}}
"""

# Top level query for retrieving a specific report
Q_REPORT_DATA = """
query {{
    reportData {{
        report(code: "{reportCode}") {{
            {innerQuery}
        }}
    }}
}}
"""

# Query for retrieving a specific fight from a specific report (subquery of Q_REPORTDATA)
Q_FIGHT_DATA = """
query {{
    reportData {{
        report(code: "{reportCode}") {{
            fights(fightIDs: {fightID}) {{
                {innerQuery}
            }}
        }}
    }}
}}
"""

IQ_REPORT_MASTER_DATA = """
masterData {
    logVersion
    actors {
        gameID
        id
        name
        server
        petOwner
        subType
        type
    }
    abilities {
        gameID
        name
        type
    }
}
"""
