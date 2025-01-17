"""
Write function which updates dictionary with defined values but only if new value more then in dict
Restriction: do not use .update() method of dictionary
Examples:
    >>> set_to_dict({'a': 1, 'b': 2, 'c': 3}, a=0, b=4)  # only b updated because new value for a less then original value
    {'a': 1, 'b': 4, 'c': 3}
    >>> set_to_dict({}, a=0)
    {a: 0}
    >>> set_to_dict({'a': 5})
    {'a': 5}
"""
from typing import Dict

def set_to_dict(dict_to_update: Dict[str, int], **items_to_set) -> Dict:
    """Updates dictionary if values provided are greater than in current dict."""
    # If no items were provided, return original dictionary.
    if not items_to_set:
        return dict_to_update

    for key, val in items_to_set.items():
        # If the key isn't in the dictionary then add it.
        if key not in dict_to_update:
            dict_to_update[key] = val
        # If the key's current value is less than specified value, replace it.
        elif dict_to_update[key] < val:
            dict_to_update[key] = val
    return dict_to_update