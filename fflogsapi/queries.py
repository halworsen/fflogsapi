'''
queries.py

Pre-baked GraphQL queries for the FFLogs API
'''

# Top level query for retrieving paginated reports
Q_REPORTPAGINATION = """
query {{
	reportData {{
		reports({filters}) {{
			{innerQuery}
		}}
	}}
}}
"""

Q_REPORTDATA = """
query {{
	reportData {{
		report(code: "{reportCode}") {{
			{innerQuery}
		}}
	}}
}}
"""

Q_FIGHTDATA = """
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