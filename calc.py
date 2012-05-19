#!/usr/bin/python

import sys
from collections import namedtuple

Item = namedtuple('Item', ['name', 'price', 'quantity', 'taxable'])
tax = 0.0825  # CA

def item_price(item):
    ret = item.price * item.quantity
    return ret * (1 + tax) if item.taxable else ret

def main(args):
    global tax
    if len(args) <= 1:
        print >> sys.stderr, "Usage: file [tax]"
        return 1
    file_path = args[1]
    if len(args) > 2: tax = float(args[2])

    items = {}
    for line in open(file_path):
        chunks = line.strip().split()
        item = Item(price = float(chunks[1]),
                    quantity = float(chunks[2]),
                    taxable = chunks[3].upper() in "TAX",
                    name = " ".join(chunks[4:]))
        who_list = chunks[0].split(",")
        for who in who_list:
            items.setdefault(who, []).append(item._replace(
                    quantity=item.quantity / len(who_list)))

    for who in items:
        total = 0
        print "Costs for %s:" % who
        for item in items[who]:
            item_total = item_price(item)
            print "%-56s %7.2f x%4.2f %s %7.2f" % (
                item.name, item.price, item.quantity,
                'T' if item.taxable else 'F',
                item_total)
            total += item_total
        print "Total for %-59s %10.2f" % (who, total)
        print "-" * 80
    all_items = sum(items.values(), [])
    print "Total for %-59s %10.2f" % ("all", sum(map(item_price, all_items)))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
