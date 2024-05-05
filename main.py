from parser.work_class import WorkUaParseClass
from analysis.data_extraction import DataExtraction
from analysis.data_processing import DataProcessing
from analysis.data_visualization import DataVisualization


searches_result = [
    "/jobs-data/",
#    "/jobs-developer/",
]

if __name__ == "__main__":
    for search in searches_result:
        parser = WorkUaParseClass()
        parser.parse_all_vacancies(search, "raw_data/")

    data_extraction = DataExtraction()
    raw_data = data_extraction.data_extraction()

    processed_data = DataProcessing(raw_data).data_processing()

    data_visualization = DataVisualization(processed_data)

    data_visualization.plot_main_skills()
