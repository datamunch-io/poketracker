import os
import csv
import datetime

from pokemontcgsdk import RestClient
from pokemontcgsdk import Card
from pokemontcgsdk import Set

from src.constants import PTCG_SECRET, PROJECT_ROOT


class PokemonAPIScraper:
    __api_key = os.environ.get(PTCG_SECRET)

    def __init__(self, first_run=False):
        RestClient.configure(self.__api_key)
        if first_run:
            self.cards = self.get_cards()
        else:
            self.cards = []

        self.sets = Set.all()

    def export_cards(self):
        if len(self.cards) == 0:
            raise ValueError('No cards currently stored.')

        card_export_list = []

        for card in self.cards:
            card_info = self.extract_card_info(card)
            card_info.update({'updated_at': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")})
            card_export_list.append(card_info)

        with open(os.path.join(PROJECT_ROOT, f'data/card_export_{str(datetime.date.today())}.csv'), 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=card_export_list[0].keys())
            writer.writeheader()
            writer.writerows(card_export_list)

    @staticmethod
    def extract_card_info(card: Card):
        print(card.name)

        card_info = {
            'card_id': card.id,
            'card_name': card.name,
            'card_set': card.set.name,
            'card_set_code': card.set.ptcgoCode,
            'rarity': card.rarity,
            'card_print_number': card.number,
            'set_printed_total': card.set.printedTotal
        }
        if card.tcgplayer and card.tcgplayer.prices:
            card_info.update(
                {
                    'tcg_holo_high': card.tcgplayer.prices.holofoil.high if card.tcgplayer.prices.holofoil else 0,
                    'tcg_holo_mid': card.tcgplayer.prices.holofoil.mid if card.tcgplayer.prices.holofoil else 0,
                    'tcg_holo_market': card.tcgplayer.prices.holofoil.market if card.tcgplayer.prices.holofoil else 0,
                    'tcg_holo_low': card.tcgplayer.prices.holofoil.low if card.tcgplayer.prices.holofoil else 0,
                    'tcg_revhol_high': card.tcgplayer.prices.reverseHolofoil.high if card.tcgplayer.prices.reverseHolofoil else 0,
                    'tcg_revhol_low': card.tcgplayer.prices.reverseHolofoil.low if card.tcgplayer.prices.reverseHolofoil else 0,
                    'tcg_revhol_mid': card.tcgplayer.prices.reverseHolofoil.mid if card.tcgplayer.prices.reverseHolofoil else 0,
                    'tcg_revhol_market': card.tcgplayer.prices.reverseHolofoil.market if card.tcgplayer.prices.reverseHolofoil else 0,
                    'tcg_first_ed_holo_high': card.tcgplayer.prices.firstEditionHolofoil.high if card.tcgplayer.prices.firstEditionHolofoil else 0,
                    'tcg_first_ed_holo_mid': card.tcgplayer.prices.firstEditionHolofoil.mid if card.tcgplayer.prices.firstEditionHolofoil else 0,
                    'tcg_first_ed_holo_low': card.tcgplayer.prices.firstEditionHolofoil.low if card.tcgplayer.prices.firstEditionHolofoil else 0,
                    'tcg_first_ed_holo_market': card.tcgplayer.prices.firstEditionHolofoil.market if card.tcgplayer.prices.firstEditionHolofoil else 0,
                    'tcg_first_ed_normal_high': card.tcgplayer.prices.firstEditionNormal.high if card.tcgplayer.prices.firstEditionNormal else 0,
                    'tcg_first_ed_normal_mid': card.tcgplayer.prices.firstEditionNormal.mid if card.tcgplayer.prices.firstEditionNormal else 0,
                    'tcg_first_ed_normal_low': card.tcgplayer.prices.firstEditionNormal.low if card.tcgplayer.prices.firstEditionNormal else 0,
                    'tcg_first_ed_normal_market': card.tcgplayer.prices.firstEditionNormal.market if card.tcgplayer.prices.firstEditionNormal else 0,
                    'tcg_normal_high': card.tcgplayer.prices.normal.high if card.tcgplayer.prices.normal else 0,
                    'tcg_normal_mid': card.tcgplayer.prices.normal.mid if card.tcgplayer.prices.normal else 0,
                    'tcg_normal_low': card.tcgplayer.prices.normal.low if card.tcgplayer.prices.normal else 0,
                    'tcg_normal_market': card.tcgplayer.prices.normal.market if card.tcgplayer.prices.normal else 0})
        else:
            print(f'No prices for {card.name} - {card.set.name}')

        return card_info

    @staticmethod
    def get_cards():
        return Card.all()

    @staticmethod
    def get_cards_by_set(set_name):
        query = f'set.name:{set_name}'
        return Card.where(q=query)

    @staticmethod
    def get_standard_legal_cards():
        query = f'legalities.standard:legal'
        return Card.where(q=query)

    @staticmethod
    def get_sets():
        return Set.all()



