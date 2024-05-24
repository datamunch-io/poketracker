from src.scraper import PokemonAPIScraper


def main():
    scraper = PokemonAPIScraper(first_run=True)
    scraper.export_cards()


if __name__ == '__main__':
    main()
    input('Complete')
