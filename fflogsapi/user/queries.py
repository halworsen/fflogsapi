# Query to retrieve information about the current user
Q_CURRENT_USER = '''
query {{
    userData {{
        currentUser {{
            {innerQuery}
        }}
    }}
}}
'''

# Retrieve information about a specific user
Q_USER = '''
query {{
    userData {{
        user(id: {userID}) {{
            {innerQuery}
        }}
    }}
}}
'''
