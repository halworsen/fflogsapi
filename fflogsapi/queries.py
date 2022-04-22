'''
queries.py

Pre-baked GraphQL queries for the FFLogs API
'''

# Top level query for retrieving paginated reports
Q_PAGINATED_REPORTS = """
query {{
	reportData {{
		reports(guildID: {guildID}, page: {page}) {{
			has_more_pages
			{innerQuery}
		}}
	}}
}}
"""

# One full page of report metadata
# Args: guildID, page
Q_INNER_REPORTS = """
data {
    owner { id, name }
    code
	title
    startTime
    endTime
}
"""

# Fight metadata in a single page of reports
Q_INNER_FIGHTS_META = """
data {
	code
	fights {
		id
		difficulty
		startTime
		endTime
	}
}
"""

# Roughly generic fight info for every report in a page
# Args: guildID, page
Q_INNER_FIGHTS_DETAIL = """
data {
	code
	fights {
		id
		name
		kill
		fightPercentage
	}
}
"""