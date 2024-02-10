from json import dump, loads
from typing import Dict

import pandas as pd
import os

from config import PATH_TO_DIR_FILES, PATH_TO_DIR_FIXTURES

pd.set_option('display.max_columns', 50)

FILENAME = 'questions.xlsx'
DELIMITER_ANSWER_OPTIONS = '#'
FILENAME_FIXTURES = 'questions_fixtures.json'
PATH_TO_FIXTURES = os.path.join(PATH_TO_DIR_FIXTURES, FILENAME_FIXTURES)


def load_data(filename: str, path_to_dir_files: str, extension: str, delimiter: str | None = None) -> pd.DataFrame:
    """
    Function for loading data from files
    :param filename: file name
    :param path_to_dir_files: file storage directory
    :param extension: file type excel or csv
    :param delimiter: column separator in a .csv file or answer separator in Excel
    :return None:
    """
    path_to_file = os.path.join(path_to_dir_files, filename)
    if not os.path.exists(path_to_file):
        raise FileNotFoundError(f'File {filename} does not exist')

    if extension not in ['excel', 'csv']:
        raise ValueError('Invalid extension')

    if not delimiter:
        delimiter = ','

    if extension == 'csv':
        df_ = pd.read_csv(path_to_file, delimiter=delimiter, index_col=0)
    else:
        df_ = pd.read_excel(path_to_file, index_col=0)

    return df_


def prepare_df_from_excel(df_: pd.DataFrame) -> Dict:
    data_dict = {}
    for index, row in df_.iterrows():
        data_dict[index] = {
            'question': row.iloc[0],
            'answer_options': row.iloc[1],
            'true_answer': row.iloc[2]
        }
    return data_dict


def save_to_json(data: Dict, filename: str) -> None:
    with open(os.path.join(PATH_TO_DIR_FIXTURES, filename), 'w', encoding='utf-8') as f:
        dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    df = load_data(FILENAME, PATH_TO_DIR_FILES, 'excel', DELIMITER_ANSWER_OPTIONS)
    result = prepare_df_from_excel(df)
    save_to_json(result, FILENAME_FIXTURES)
