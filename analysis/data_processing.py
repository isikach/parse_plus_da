import re

import numpy as np
import pandas as pd


class DataProcessing:

    JOBS_WITH_PYTHON = ["data", "python", "backend", "fullstack"]

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def data_processing(self) -> pd.DataFrame:
        self.fix_company_type_column()
        self.fix_additional_column()
        self.fix_company_size_column()
        self.fix_english_level_column()
        self.add_job_group_by_title()
        self.add_work_schedule()
        self.add_education_restriction()
        self.add_required_experience()
        self.add_is_pythonic_param()
        return self.df

    def fix_company_type_column(self) -> None:
        self.df["company_type"] = self.df["company_type"].str.replace(";", "")

    def fix_additional_column(self) -> None:
        self.df["additional"] = self.df["additional"].str.replace(",", ".").str.lower().str.split(".")

    def fix_company_size_column(self) -> None:
        size_mapping = {
            "менше 10 співробітників": "startup (10< employees)",
            "10–50 співробітників": "small (10 - 50 employees)",
            "50–250 співробітників": "medium-low (50 - 250 employees)",
            "250–1000 співробітників": "medium-high (250 - 1000 employees)",
            "більше 1000 співробітників": "big (<1000 employees)"
        }

        self.df["company_size"] = self.df["company_size"].map(size_mapping)

    def fix_english_level_column(self) -> None:
        self.df["english_level"] = self.df.english_level.map(DataProcessing.english_level_coding)

    def add_required_experience(self) -> None:
        self.df["experience_years"] = self.df.additional.apply(DataProcessing.required_experience)

    def add_work_schedule(self) -> None:
        self.df["work_schedule"] = self.df["additional"].apply(DataProcessing.work_schedule)

    def add_education_restriction(self) -> None:
        self.df["education"] = self.df["additional"].map(DataProcessing.education_restriction)

    def add_job_group_by_title(self) -> None:
        self.df["job_type"] = self.df["title"].apply(DataProcessing.group_by_tech)

    def add_is_pythonic_param(self) -> None:
        self.df["is_pythonic"] = self.df['job_type'].isin(DataProcessing.JOBS_WITH_PYTHON)

    @staticmethod
    def group_by_tech(job_title: str) -> str:
        job_title = job_title.lower().strip().replace("-", " ")
        if ".net" in job_title:
            return ".net"
        if any(keyword in job_title for keyword in ["flutter", "android", "ios"]):
            return "mobile"
        if "node.js" in job_title:
            return "node.js"
        if any(keyword in job_title for keyword in ["javascript", "react", "js", "angular"]):
            return "javascript"
        if "java " in job_title:
            return "java"
        if "python" in job_title:
            return "python"
        if "front end" in job_title or "frontend" in job_title:
            return "frontend"
        if any(keyword in job_title for keyword in ["php", "laravel", "symfony"]):
            return "php"
        if "wordpress" in job_title:
            return "wordpress"
        if any(keyword in job_title for keyword in ["data", "аналітик", "analyst"]):
            return "data"
        if any(keyword in job_title for keyword in ["безпеки", "захисту", "security"]):
            return "cyber sec"
        if "unity" in job_title:
            return "unity"
        if "1с" in job_title or "1c" in job_title:
            return "1с"
        if "embedded" in job_title:
            return "embedded"
        if "back end" in job_title or "backend" in job_title:
            return "backend"
        if "fullstack" in job_title or "full stack" in job_title:
            return "fullstack"
        return job_title

    @staticmethod
    def english_level_coding(restriction: str | None) -> str:
        if restriction is np.NaN:
            return "no info"
        restriction = restriction.lower()
        if "англійська — початковий" in restriction:
            return "A2"
        if "aнглійська — середній" in restriction:
            return "B1"
        if "англійська — вище середнього" in restriction:
            return "B2"
        if "англійська — просунутий" in restriction:
            return "C1"
        if "англійська — вільно" in restriction:
            return "C2"
        return "no info"

    @staticmethod
    def required_experience(lst: list) -> int | str:
        for item in lst:
            expected_years = re.findall(r'\d+', item)
            if expected_years:
                return expected_years[0]
        return "no info"

    @staticmethod
    def work_schedule(lst: list) -> str:
        lst = [item.strip() for item in lst]
        if "повна зайнятість" in lst and "неповна зайнятість" in lst:
            return "has both options"
        elif "повна зайнятість" in lst:
            return "full-time"
        elif "неповна зайнятість" in lst:
            return "part-time"
        else:
            return "unknown"

    @staticmethod
    def education_restriction(lst: list) -> str:
        lst = [item.strip() for item in lst]
        if "вища освіта" in lst:
            return "Higher Education"
        return "Not Necessary"
