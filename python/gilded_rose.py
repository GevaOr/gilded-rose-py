# -*- coding: utf-8 -*-

class GildedRose(object):
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"

    SPECIAL_CASES = [
        AGED_BRIE,
        BACKSTAGE_PASSES,
        # SULFURAS,
    ]

    CONJURED_PREFIX = "Conjured"

    def __init__(self, items):
        self.items = items

    def _decrease_item_quality_by(self, item, decrease_by):
        outcome = item.quality - decrease_by
        if outcome >= 0:
            if outcome > 50:
                outcome = 50
            item.quality = outcome
            return
        item.quality = 0

    def _decrease_item_sell_in_by(self, item, decrease_by):
        item.sell_in -= decrease_by

    def _is_item_special_case(self, item):
        if item.name in self.SPECIAL_CASES or item.name.startswith(self.CONJURED_PREFIX):
            return True
        return False

    def _is_item_expired(self, item):
        return item.sell_in < 0

    def _is_item_max_quality(self, item):
        return item.quality >= 50

    def _updated_backstage_pass_decrease(self, item, current_decrease_amount):
        if item.sell_in < 0:
            current_decrease_amount = item.quality
            return current_decrease_amount
        if item.sell_in < 10:
            current_decrease_amount -= 1
        if item.sell_in < 5:
            current_decrease_amount -= 1
        return current_decrease_amount

    def update_quality(self):
        for item in self.items:
            time_passed = 1
            quality_decrease_amount = 1
            if item.name == self.SULFURAS:
                time_passed = 0
                quality_decrease_amount = 0
            self._decrease_item_sell_in_by(item, time_passed)
            if self._is_item_special_case(item):
                if item.name.startswith(self.CONJURED_PREFIX):
                    quality_decrease_amount *= 2

                elif not self._is_item_max_quality(item):
                    quality_decrease_amount = -1
                    if item.name == self.BACKSTAGE_PASSES:
                        quality_decrease_amount = self._updated_backstage_pass_decrease(
                            item, quality_decrease_amount)
                else:
                    quality_decrease_amount = 0
                    if item.name == self.BACKSTAGE_PASSES:
                        quality_decrease_amount = self._updated_backstage_pass_decrease(
                            item, quality_decrease_amount)

            if self._is_item_expired(item):
                quality_decrease_amount *= 2

            self._decrease_item_quality_by(item, quality_decrease_amount)

    # def update_quality(self):
    #     for item in self.items:
    #         if item.name != self.AGED_BRIE and item.name != self.BACKSTAGE_PASSES:
    #             if item.quality > 0:
    #                 if item.name != self.SULFURAS:
    #                     item.quality -= 1
    #                 if item.name.startswith(self.CONJURED_PREFIX):
    #                     item.quality -= 1
    #         else:
    #             if item.quality < 50:
    #                 item.quality = item.quality + 1
    #                 if item.name == self.BACKSTAGE_PASSES:
    #                     if item.sell_in < 11:
    #                         if item.quality < 50:
    #                             item.quality = item.quality + 1
    #                     if item.sell_in < 6:
    #                         if item.quality < 50:
    #                             item.quality = item.quality + 1
    #         if item.name != self.SULFURAS:
    #             item.sell_in -= 1
    #         if item.sell_in < 0:
    #             if item.name != self.AGED_BRIE:
    #                 if item.name != self.BACKSTAGE_PASSES:
    #                     if item.quality > 0:
    #                         if item.name != self.SULFURAS:
    #                             if item.name.startswith(self.CONJURED_PREFIX):
    #                                 item.quality -= 1
    #                             item.quality -= 1
    #                 else:
    #                     item.quality = item.quality - item.quality
    #             else:
    #                 if item.quality < 50:
    #                     item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
