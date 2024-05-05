import pickle
import pandas as pd
from dataclasses import dataclass
from pathlib import Path

from src.mlservice.model.model import *
from src.mlservice.adapters.repository import IMachineLearningRepository


class TodoEntryNotFound(Exception):
    pass


@dataclass
class MachineLearningRepository(IMachineLearningRepository):
    storage_dir: str

    def get_user(self, userid: str) -> User:
        for entry_file_path in Path(self.storage_dir).iterdir():
            with open(entry_file_path, mode="rb") as entry_file:
                entry: User = pickle.load(entry_file)
                if entry.userid == userid:
                    return entry
        raise TodoEntryNotFound(f"User with id {userid} not found")

    def get_posts(self, userid: str) -> list[Post]:
        entries: list[Post] = []
        for entry_file_path in Path(self.storage_dir).iterdir():
            with open(entry_file_path, mode="rb") as entry_file:
                entry: Post = pickle.load(entry_file)
                if entry.userid == userid:
                    entries.append(entry)
        return entries

    def get_last_posts(self) -> list[str]:
        entries: list[str] = []
        for entry_file_path in Path(self.storage_dir).iterdir():
            with open(entry_file_path, mode="rb") as entry_file:
                entry: Post = pickle.load(entry_file)
                entries.append(entry.content)
        return entries
    
@dataclass
class MockMachineLearningRepository(IMachineLearningRepository):

    def get_user(self, userid: str) -> User:
        pass

    def get_posts(self, userid: str) -> list[Post]:
        pass

    def get_last_posts(self) -> list[str]:
        # Mock loading data from an Excel file
        try:
            df = pd.read_excel('training_models/test1.xlsx')
            text_list = df['Text'].tolist()
            return text_list
        except Exception as e:
            print(f"Error loading text from Excel file: {e}")
            return []

