# Top level query for retrieving paginated reports
Q_REPORT_PAGINATION = '''
query {{
    reportData {{
        reports({filters}) {{
            {innerQuery}
        }}
    }}
}}
'''

# Top level query for retrieving a specific report
Q_REPORT_DATA = '''
query {{
    reportData {{
        report(code: "{reportCode}") {{
            {innerQuery}
        }}
    }}
}}
'''

# Query for retrieving a specific fight from a specific report (subquery of Q_REPORTDATA)
Q_FIGHT_DATA = '''
query {{
    reportData {{
        report(code: "{reportCode}") {{
            fights(fightIDs: {fightID}) {{
                {innerQuery}
            }}
        }}
    }}
}}
'''

# Report-internal query for the report's log version
IQ_REPORT_LOG_VERSION = '''
masterData {
    logVersion
}
'''

# Report-internal query for the actor data contained in the report
IQ_REPORT_ACTORS = '''
masterData {
    actors {
        gameID
        id
        name
        server
        petOwner
        subType
        type
    }
}
'''

# Report-internal query for all abilities seen in the report
IQ_REPORT_ABILITIES = '''
masterData {
    abilities {
        gameID
        name
        type
    }
}
'''

# Report-internal query for phase information contained in the report
IQ_REPORT_PHASES = '''
phases {
    encounterID
    separatesWipes
    phases {
        id
        isIntermission
        name
    }
}
'''
