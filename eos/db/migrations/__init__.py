"""
The migration module includes migration logic to update database scheme and/or
data for the user database.

To create a migration, simply create a file upgrade<migration number>.py and
define an upgrade() function with the logic. Please note that there must be as
many upgrade files as there are database versions (version 5 would include
upgrade files 1-5)
"""
