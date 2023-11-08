def validate_order(menu, order_details):
    for item_id in order_details.keys():
        if item_id not in menu.index:
            return False
    return True