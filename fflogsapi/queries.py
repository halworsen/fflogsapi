'''
queries.py

Pre-baked GraphQL queries for the FFLogs API
'''

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

# Retrieves only metadata from pages
Q_REPORT_PAGE_META = """
current_page
has_more_pages
from
to
data {
	code
}
"""