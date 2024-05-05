from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


@dataclass
class Vacancy:
    title: str
    company_type: str
    company_size: str
    skills: str
    additional: str
    views_count: int
    english_level: str = None


class BaseParser(ABC):
    @abstractmethod
    def __init__(self, url: str):
        self.vacancies = []
        self.url = url

    @staticmethod
    @abstractmethod
    def parse_company_info(soup: BeautifulSoup) -> list[str]:
        pass

    @staticmethod
    @abstractmethod
    def parse_skills(soup: BeautifulSoup) -> list[str]:
        pass

    @staticmethod
    @abstractmethod
    def additional_info(soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_reviews(soup: BeautifulSoup) -> int:
        pass

    @staticmethod
    @abstractmethod
    def parse_english_level(soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def parse_single_vacancy(self, soup: BeautifulSoup) -> None:
        pass

    @staticmethod
    @abstractmethod
    def find_last_page(soup: BeautifulSoup) -> int:
        pass

    @abstractmethod
    def save_results(self, file_name):
        pass

    @abstractmethod
    def parse_all_vacancies(self, part: str) -> None:
        pass
