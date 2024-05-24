from google.cloud import bigquery 

from src import constants 


class Poketracker:
    def __init__(self):
        self.client = self.initialize_bq_client()
        self.searchables = self.get_searchables()
        
    def get_searchables(self):
        # TODO: Create a cards table to separate the searchables and card prices.
        query = f"""
            SELECT card_id, CONCAT(card_name, '-', card_set_code, ' ', card_print_number,  '/', set_printed_total) AS searchable
            FROM {constants.DATASET_ID}.{constants.TABLES.get('prices')}
        """
        
        job = self.client.query(query=query)
        results = job.result()
        return {row.card_id: row.searchable for row in results}
        
    @staticmethod 
    def initialize_bq_client():
        return bigquery.Client(project=constants.PROJECT_NAME)
        