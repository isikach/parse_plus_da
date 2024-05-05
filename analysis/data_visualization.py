import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataVisualization:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df_pythonic = self.df[self.df['is_pythonic']]

    def plot_top_15_jobs(self):

        top_job_types = self.df['job_type'].value_counts().head(15).index.tolist()
        filtered_data = self.df[self.df['job_type'].isin(top_job_types)]

        sns.countplot(
            x="job_type",
            data=filtered_data,
            order=top_job_types,
            hue="is_pythonic"
        )
        plt.xticks(rotation=45)
        plt.show()

    def plot_by_spheres(self) -> None:
        plt.figure(figsize=(12, 8))
        sns.histplot(data=self.df_pythonic, y="company_type")
        plt.show()

    def plot_by_company_type(self) -> None:
        sorting = [
            "startup (10< employees)",
            "small (10 - 50 employees)",
            "medium-low (50 - 250 employees)",
            "medium-high (250 - 1000 employees)",
            "big (<1000 employees)"
        ]

        self.df_pythonic.loc[:, "company_size"] = pd.Categorical(
            self.df_pythonic["company_size"],
            categories=sorting,
            ordered=True
        )

        sns.histplot(data=self.df_pythonic.sort_values(by="company_size"), y="company_size")
        plt.ylabel("Company Size")
        plt.xlabel("Frequency")
        plt.show()

    def plot_main_skills(self) -> None:
        skills = self.skills_processing()
        visualisation_skills = pd.Series(skills).value_counts()
        top_15 = visualisation_skills.head(15)

        df_top_15 = pd.DataFrame({'Skill': top_15.index, 'Count': top_15.values})

        sns.barplot(y='Skill', x='Count', data=df_top_15)
        plt.xticks(rotation=90)
        plt.show()

    def skills_processing(self) -> list:
        skills_all = self.df_pythonic.skills.to_list()
        skills_processed = []
        for skill in skills_all:
            if skill:
                for s in str(skill).split(","):
                    if s:
                        skills_processed.append(s.strip())
        return skills_processed
