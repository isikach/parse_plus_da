import csv
import os
import re
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from parser.base_class import BaseParser, Vacancy


class WorkUaParseClass(BaseParser):

    def __init__(self):
        self.vacancies: List[Vacancy] = []
        self.base_url = "https://www.work.ua/"

    @staticmethod
    def parse_company_info(soup: BeautifulSoup) -> list[str]:
        c_type = None
        c_size = None
        company_info = soup.find_all("span", {"class": "mt-xs text-default-7"})
        for c_info in company_info:
            c_type = c_info.text.strip().split("\n")[0].strip()
            try:
                c_size = c_info.text.strip().split("\n")[1].strip().replace("&nbsp;", " ")
            except IndexError:
                c_size = None
        return [c_type, c_size]

    @staticmethod
    def parse_skills(soup: BeautifulSoup) -> str:
        vac_skills = ""
        skills = soup.find_all("span", {"class": "ellipsis"})
        if skills:
            for skill in skills:
                vac_skills += f", {skill.text}"
        return vac_skills

    @staticmethod
    def additional_info(soup: BeautifulSoup) -> str:
        additional = soup.find_all("p", {"class": "text-indent mt-sm"})[-1]
        return additional.text.strip()

    @staticmethod
    def parse_reviews(soup: BeautifulSoup) -> int:
        reviews = soup.find("span", {"class": "strong-600"}).text
        return int(re.findall(r'\d+', reviews)[0])

    @staticmethod
    def parse_english_level(soup: BeautifulSoup) -> str:
        eng_level = soup.find("p", {"class": "text-indent add-top-sm"})
        if eng_level:
            return eng_level.text.strip().replace("\n", "")

    def parse_single_vacancy(self, soup: BeautifulSoup) -> None:
        company_type, company_size = WorkUaParseClass.parse_company_info(soup)
        single_job = Vacancy(
            title=soup.select_one("h1").text,
            company_type=company_type,
            company_size=company_size,
            skills=WorkUaParseClass.parse_skills(soup),
            additional=WorkUaParseClass.additional_info(soup),
            views_count=WorkUaParseClass.parse_reviews(soup),
            english_level=WorkUaParseClass.parse_english_level(soup),
        )
        self.vacancies.append(single_job)

    @staticmethod
    def get_urls_list(url: str, page: int) -> List[str]:
        payload = {"page": page}
        response = requests.get(url, params=payload)
        soup = BeautifulSoup(response.text, "html.parser")
        urls = soup.find_all("h2", attrs={"class": "cut-top cut-bottom"})
        return [url.select_one('a')['href'] for url in urls]

    def parse_page(self, url: str, page: int) -> None:
        page_url = urljoin(self.base_url, url)
        all_vacancies_from_page = self.get_urls_list(page_url, page)
        for vac_url in all_vacancies_from_page:
            response = requests.get(urljoin(self.base_url, vac_url))
            soup = BeautifulSoup(response.text, "html.parser")
            self.parse_single_vacancy(soup)

    @staticmethod
    def find_last_page(soup: BeautifulSoup) -> int:
        pagination = soup.find_all("a", attrs={"class": "ga-pagination-default pointer-none-in-all"})
        return int(pagination[-1].text)

    def save_results(self, file_name):
        directory = os.path.dirname(file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "title",
                "company_type",
                "company_size",
                "skills",
                "additional",
                "views_count",
                "english_level",
            ])
            for vacancy in self.vacancies:
                writer.writerow(
                    [
                        vacancy.title,
                        vacancy.company_type,
                        vacancy.company_size,
                        vacancy.skills,
                        vacancy.additional,
                        vacancy.views_count,
                        vacancy.english_level,
                    ]
                )

    def parse_all_vacancies(self, part: str, path: str = "../raw_data/") -> None:
        url = urljoin(self.base_url, part)
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        last_page = self.find_last_page(soup)
        for page in range(1, last_page + 1):
            self.parse_page(url, page)
            print(f"Parsing page {page}")
        name = path + part.replace("/", "") + ".csv"
        self.save_results(name)
