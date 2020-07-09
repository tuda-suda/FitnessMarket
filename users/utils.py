from typing import Dict

def qs_to_filters(querystrings: Dict) -> Dict:
    """
    Parse querystrings to model filter fields
    :param querystrings: a querystring dict from request.GET
    :return: a dict of model filters
    """
    filters = {}

    for query in querystrings:
        if query == 'priceFrom':
            filter_field = 'cost__gte'
        elif query == 'priceTo':
            filter_field = 'cost__lte'
        else:
            filter_field = query

        filters[filter_field] = querystrings[query]

    return filters