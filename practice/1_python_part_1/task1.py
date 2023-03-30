"""
Write function which deletes defined element from list.
Restriction: Use .pop method of list to remove item.
Examples:
    >>> delete_from_list([1, 2, 3, 4, 3], 3)
    [1, 2, 4]
    >>> delete_from_list(['a', 'b', 'c', 'b', 'd'], 'b')
    ['a', 'c', 'd']
    >>> delete_from_list([1, 2, 3], 'b')
    [1, 2, 3]
    >>> delete_from_list([], 'b')
    []
"""
from typing import List, Any

def delete_from_list(list_to_clean: List, item_to_delete: Any) -> List:
    """Removes the specified item from the list."""
    for ind, item in enumerate(list_to_clean):
        # If current item in list is the item to delete, remove from list.
        if item == item_to_delete:
            list_to_clean.pop(ind)
    return list_to_clean