def calculate_total(order, menu):
    total = 0
    for i, row in order.iterrows():
        item_id = row["SpeiseID"]
        quantity = row["Menge"]
        price = menu.loc[item_id, "Preis"]
        total += price * quantity
    return total

def generate_invoice(order, menu, tip=0):
    total = calculate_total(order, menu)
    net_price = total
    tax_rate = 0.19  
    tax_amount = total * tax_rate
    total_price = total + tax_amount
    if tip > 0:
        total_price += tip

    invoice = {
        "Gerichte": order,
        "Nettopreis": net_price,
        "MwSt.": tax_amount,
        "Bruttopreis": total_price,
        "Trinkgeld": tip
    }
    return invoice