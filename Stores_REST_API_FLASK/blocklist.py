

"""
This file just contains the blocklist of JWT tokens. It will be imported by app and the logout
resources so that the tokens can be added to the blocklist.py when the user logouts.
"""

BlockList = set()
