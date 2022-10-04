# import standard library modules
from getpass import getpass

# import the ArcGIS API for Python
from arcgis.gis import GIS, User


def recursive_delete(items):
    """Deletes all items and their dependents."""
    for item in items:
        try:
            dry_run = item.delete(dry_run=True)
        
            if dry_run["can_delete"]:
                item.delete()
            elif dry_run["details"]["message"] == f"Unable to delete item {item.id}. Delete protection is turned on.":
                item.protect(enable=False)
                item.delete()
            elif dry_run["details"]["message"] == "Unable to delete item. This service item has a related Service item":
                recursive_delete(dry_run["details"]["offending_items"])
        except TypeError:
            print(f"Item ({item.id}) no longer exists or is inaccessible.")
    return


# instantiate GIS object with admin credentials
gis = GIS("https://arcgis.com", "<admin_username>", getpass("Enter admin password > "))

# instantiate User object with the old user's username
old_member = User(gis, "<old_username>")

# delete all items in root folder
recursive_delete(old_member.items(max=1000))

# delete items in all other folders
for f in old_member.folders:
    recursive_delete(old_member.items(folder=f, max=1000))