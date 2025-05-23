import json
import csv

class CSVService():
    """Service for converting JSON to    CSV and vice versa"""

    def __init__(self):
        self.questionnaire_header_fields = [
            "id", "external_id", "calculation_type", "route_to_after_completion",
            "title", "subtitle", "description", "celebrate", "celebrate_text", "confetti",
            "default_language", "show_question", "disable_progress_bar",
            "instructions_header", "instructions_back_button", "instructions_next_button",
            "survey_id", "new", "allow_instructions", "supported_languages"
        ]

        self.questionnaire_metadata_fields = [
            "questionnaire_instructions", "calculated_variables",
            "data_points", "question_groups"
        ]

        self.question_fields = [
            "id", "external_id", "type", "minimum", "maximum", "default_value", "step",
            "minimum_length", "maximum_length", "mandatory", "confirm_skip", "scoring",
            "footer", "info_text", "description", "save_answer", "short_name",
            "binah_question_id", "no_value", "title", "subtitle", "minimum_label",
            "title_hidden", "maximum_label", "placeholder", "orientation", "data_label",
            "allow_verify", "allow_verify_text", "decimal_places", "overlay", "camera",
            "allow_instructions", "allow_recording_instructions", "recording_instructions",
            "restrict_video_length", "max_video_time", "conditional_logic",
            "question_group_id", "show_as_dropdown", "restricted", "routing_logic"
        ]

        self.option_fields = [
            "id", "index", "question_id", "score", "text", "external_id"
        ]


    def convert_csv_to_json(self, csv_file):
        """Convert a CSV file to a JSON object"""
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def _clean_list_strings(self,lst):
        """Remove leading/trailing quotes from each string in the list"""
        return lst
        updated_list = []
        if isinstance(lst, list):
            for s in lst:
                if isinstance(s, str):
                    s = s.strip('"').strip("'")
                updated_list.append(s)
            print(f"UPDATED LIST: {updated_list}")
            return updated_list
        return lst
    
    def convert_questionnaire_json_to_csv(self, json_data: dict, output_path: str = "weguide_formatted.csv"):
        """
        Converteert een vragenlijst in JSON (WeGuide-formaat) naar een CSV-bestand
        conform de vereisten van het WeGuide-importsysteem.
        """
        with open(output_path, mode='w', newline='\n', encoding='utf-8') as csvfile:

        # with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Header section
            for field in self.questionnaire_header_fields:
                value = json_data.get(field, "")
                if isinstance(value, str):
                    value = value.strip('"').strip("'")
                if isinstance(value, list):
                    value = str(value)
                    value = value.strip('"').strip("'")
                if isinstance(value, dict):
                    value = str(value)
                    value = value.replace(',', '=>[],')
                    value = value.strip('"').strip("'")

                print(f"Value: {value}")
                if isinstance(value, (list, dict)):
                    value = json.dumps(self._clean_list_strings(value), ensure_ascii=False)
                    if value.startswith('"') and value.endswith('"') and ',' not in value:
                        value = value[1:-1]  # remove surrounding quotes if any

                # if isinstance(value, (list, dict)):
                #     value = json.dumps(value)
                writer.writerow([field, value])

            # Metadata section
            for field in self.questionnaire_metadata_fields:
                value = json_data.get(field, "")
                
                if isinstance(value, str):
                    value = value.strip('"').strip("'")
                if isinstance(value, list):
                    value = str(value)
                    value = value.strip('"').strip("'")
                if isinstance(value, dict):
                    value = str(value)
                    value = value.replace(',', '=>[],')
                    value = value.strip('"').strip("'")
                print(f"Value: {value}")

                if isinstance(value, (list, dict)):
                    value = json.dumps(self._clean_list_strings(value), ensure_ascii=False)
                    if value.startswith('"') and value.endswith('"') and ',' not in value:
                        value = value[1:-1]  # remove surrounding quotes if any

                # if isinstance(value, (list, dict)):
                #     value = json.dumps(value)
                writer.writerow([field, value])

            # Questions header
            writer.writerow([])
            # writer.writerow(["# Questions"])
            writer.writerow(self.question_fields)

            for question in json_data.get("questions", []):
                row = [question.get(field, "") for field in self.question_fields]
                writer.writerow(row)

                # Options per question
                if "options" in question and isinstance(question["options"], list):
                    writer.writerow([""] + self.option_fields)
                    for opt in question["options"]:
                        opt_row = [""] + [opt.get(f, "") for f in self.option_fields]
                        writer.writerow(opt_row)

        print(f"WeGuide CSV geëxporteerd naar: {output_path}")
        return self.read_csv_as_string(output_path)

    def read_csv_as_string(self, file_path: str) -> str:
        """
        Reads the entire contents of a CSV file and returns it as a single string.
        """
        with open(file_path, mode='r', encoding='utf-8') as f:
            return f.read()