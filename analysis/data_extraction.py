import os

import pandas as pd


class DataExtraction:
    @staticmethod
    def data_extraction(source: str = "../raw_data/") -> pd.DataFrame:
        sources = os.listdir(source)
        raw_data = pd.DataFrame()

        for source in sources:
            df = pd.read_csv(f"../raw_data/{source}")
            raw_data = pd.concat([df, raw_data], ignore_index=True)

        return raw_data
