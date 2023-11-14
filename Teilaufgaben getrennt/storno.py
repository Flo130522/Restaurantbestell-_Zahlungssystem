def cancel_order(order_list, order_id):
    order_list.loc[order_list["ID"] == order_id, "Status"] = "storno"