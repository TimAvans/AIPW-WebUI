from enum import Enum

class CSVOutput():
    id: int
    external_id: str
    calculation_type: str
    route_to_after_completion: str
    title: str
    subtitle: str
    description: str
    celebrate: bool
    celebrate_text: str
    confetti: bool
    default_language: str
    show_question: bool
    disable_progress_bar: bool
    instructions_header: str
    instructions_back_button: str
    instructions_next_button: str
    survey_id: str
    new: bool
    allow_instructions: bool
    supported_language: list[str]
    questionaire_instructions: list[str]
    calculated_variables: str # list[list[list[str]]] 
    data_points: str
    question_groups: str


class QuestionType(str, Enum):
    SingleChoiceQuestion = "SingleChoiceQuestion"              # Single-select question with multiple options
    MultipleChoiceQuestion = "MultipleChoiceQuestion"          # Multi-select question with multiple options
    RangeSliderQuestion = "RangeSliderQuestion"                # Slider for selecting values in a range
    TextQuestion = "TextQuestion"                              # Free text input field
    NumberQuestion = "NumberQuestion"                          # Numeric input field
    EmailQuestion = "EmailQuestion"                            # Input field for email addresses
    Instruction = "Instruction"                                # Informational text (not a question)
    DateQuestion = "DateQuestion"                              # Date selection field
    TimeQuestion = "TimeQuestion"                              # Time selection field
    DateTimeQuestion = "DateTimeQuestion"                      # Combined date and time selection
    YearQuestion = "YearQuestion"                              # Year selection field
    PhotoQuestion = "PhotoQuestion"                            # Photo upload field
    VideoQuestion = "VideoQuestion"                            # Video upload field
    SignatureQuestion = "SignatureQuestion"                    # Signature capture field
    FileUploadQuestion = "FileUploadQuestion"                  # Generic file upload field
    BinahQuestion = "BinahQuestion"                            # For biometric data
    HappyTechQuestion = "HappyTechQuestion"                    # For mood/emotion tracking

class QuestionOptionModel:
    id: int
    index: str
    question_id: str
    score: float
    text: str
    external_id: str

class QuestionModel():
    id: int
    external_id: str
    type: QuestionType #Enums
    minimum: float
    maximum: float
    minimum_length: int
    maximum_length: int
    mandatory: bool
    confirm_skip: bool
    scoring: bool
    footer: str
    info_text: str
    description: str
    save_answer: bool 
    short_name: str
    title: str
    subtitle: str
    placeholder: str
    orientation: str
    data_label: str
    conditional_logic: str # Json
    question_group_id: int
    show_as_dropdown: bool
    restricted: bool
    routing_logic: str # Json
    options: list[QuestionOptionModel]
