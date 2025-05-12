json_output = {
      "type": "json_schema",
      "json_schema": {
        "name": "weguide_questionnaire",
        "strict": True,
        "schema": {
          "type": "object",
          "required": ["id", "external_id", "calculation_type", "route_to_after_completion", "title", "subtitle", 
                       "description", "celebrate", "celebrate_text", "confetti", "default_language", "show_question", 
                       "disable_progress_bar", "instructions_header", "instructions_back_button", "instructions_next_button", 
                       "survey_id", "new", "allow_instructions", "supported_languages", "questionnaire_instructions", 
                       "calculated_variables", "data_points", "question_groups", "questions"],
          "properties": {
            "id": {
                "type": "integer", "description": "Generate a unique ID for this questionnaire"
                },
            "external_id": {"type": "string"},
            "calculation_type": {
              "type": "string",
              "enum": ["not_applicable", "summation", "mean", "percentage"]
            },
            "route_to_after_completion": {"type": "string"},
            "title": {"type": "string"},
            "subtitle": {"type": "string"},
            "description": {"type": "string"},
            "celebrate": {"type": "boolean"},
            "celebrate_text": {"type": "string"},
            "confetti": {"type": "boolean"},
            "default_language": {"type": "string"},
            "show_question": {"type": "boolean"},
            "disable_progress_bar": {"type": "boolean"},
            "instructions_header": {"type": "string"},
            "instructions_back_button": {"type": "string"},
            "instructions_next_button": {"type": "string"},
            "survey_id": {"type": "string"},
            "new": {"type": "boolean"},
            "allow_instructions": {"type": "boolean"},
            "supported_languages": {
              "type": "array",
              "items": {"type": "string"}
            },
            "questionnaire_instructions": {
              "type": "array",
              "items": {"type": "string"}
            },
            "calculated_variables": {"type": "string"},
            "data_points": {"type": "string"},
            "question_groups": {"type": "string"},
            "questions": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["id", "external_id", "type", "minimum", "maximum", "minimum_length", "maximum_length", 
                             "mandatory", "confirm_skip", "scoring", "footer", "info_text", "description", "save_answer", 
                             "short_name", "title", "subtitle", "placeholder", "orientation", "data_label", "conditional_logic", 
                             "question_group_id", "show_as_dropdown", "restricted", "routing_logic", "options"],
                "properties": {
                  "id": {"type": "integer", "description": "Generate a unique ID for this question-option"},
                  "external_id": {"type": "string"},
                  "type": {
                    "type": "string",
                    "enum": [
                      "SingleChoiceQuestion", "MultipleChoiceQuestion", "RangeSliderQuestion", "TextQuestion",
                      "NumberQuestion", "EmailQuestion", "Instruction", "DateQuestion", "TimeQuestion",
                      "DateTimeQuestion", "YearQuestion", "PhotoQuestion", "VideoQuestion", "SignatureQuestion",
                      "FileUploadQuestion", "BinahQuestion", "HappyTechQuestion"
                    ]
                  },
                  "minimum": {"type": "number"},
                  "maximum": {"type": "number"},
                  "minimum_length": {"type": "integer"},
                  "maximum_length": {"type": "integer"},
                  "mandatory": {"type": "boolean"},
                  "confirm_skip": {"type": "boolean"},
                  "scoring": {"type": "boolean"},
                  "footer": {"type": "string"},
                  "info_text": {"type": "string"},
                  "description": {"type": "string"},
                  "save_answer": {"type": "boolean"},
                  "short_name": {"type": "string"},
                  "title": {"type": "string"},
                  "subtitle": {"type": "string"},
                  "placeholder": {"type": "string"},
                  "orientation": {"type": "string"},
                  "data_label": {"type": "string"},
                  "conditional_logic": {"type": "string"},
                  "question_group_id": {"type": "integer"},
                  "show_as_dropdown": {"type": "boolean"},
                  "restricted": {"type": "boolean"},
                  "routing_logic": {"type": "string"},
                  "options": {
                    "type": "array",
                    "items": {
                      "type": "object",
                       "required": ["id", "index", "question_id", "score", "text", "external_id"],
                      "properties": {
                        "id": {"type": "integer", "description": "Generate a unique ID for this question-option"},
                        "index": {"type": "integer"},
                        "question_id": {"type": "integer", "description": "Generate a unique ID for this question"},
                        "score": {"type": "number"},
                        "text": {"type": "string"},
                        "external_id": {"type": "string"}
                      },
                    "additionalProperties": False
                    }
                  }
                },
                "additionalProperties": False
              }
            }
          },
          "additionalProperties": False
        }
      }
    }