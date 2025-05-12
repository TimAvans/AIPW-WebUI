# WeGuide Form/Questionnaire Import Technical Documentation

## Introduction

This document provides comprehensive technical documentation for the WeGuide form/questionnaire import functionality. It describes the CSV file structure, accepted values, required fields, and common failure scenarios. The document is based on analysis of the codebase and an example PHQ-9 questionnaire CSV file.

## Overview

WeGuide's platform allows users to import questionnaires through CSV files. These questionnaires (also called forms) contain various types of questions, options, validations, and other metadata. The import feature lets administrators create or update questionnaires without having to manually input each field through the user interface.

## CSV File Structure

The CSV file for questionnaire imports has multiple sections, each with its own purpose and structure:

### 1. Questionnaire Header Section

The first rows in the CSV contain the main questionnaire attributes:

```
id,21
external_id,""
calculation_type,not_applicable
route_to_after_completion,""
title,PHQ-9
subtitle,""
description,""
celebrate,false
celebrate_text,""
confetti,false
default_language,English
show_question,true
disable_progress_bar,false
instructions_header,""
instructions_back_button,""
instructions_next_button,""
survey_id,PHQ9
new,true
allow_instructions,false
supported_languages,[English]
```

### 2. Questionnaire Metadata Section

Following the header section are rows for additional questionnaire metadata:
```
questionnaire_instructions,[]
calculated_variables,"[[[""total"", ""[PHQ9_little_interest_score] + [PHQ9_hopeless_score] + [PHQ9_sleep_score] + [PHQ9_tired_score] + [PHQ9_appetite_score] + [PHQ9_feeling_bad_score] + [PHQ9_concentration_score] + [PHQ9_speed_score] + [PHQ9_dead_score]"", ""PHQ-9 Total"", 0.0, """", """"], []]]"
data_points,"{""participant""=>[], ""survey""=>[]}"
question_groups,[]
```

### 3. Question Columns Header Row

Next is a header row that defines the columns for all questions that follow:
```
id,external_id,type,minimum,maximum,default_value,step,minimum_length,maximum_length,mandatory,confirm_skip,scoring,footer,info_text,description,save_answer,short_name,binah_question_id,no_value,title,subtitle,minimum_label,title_hidden,maximum_label,placeholder,orientation,data_label,allow_verify,allow_verify_text,decimal_places,overlay,camera,allow_instructions,allow_recording_instructions,recording_instructions,restrict_video_length,max_video_time,conditional_logic,question_group_id,show_as_dropdown,restricted,routing_logic
```

### 4. Questions and Related Data

Following sections contain individual questions with their options, validations, and instructions, formatted in specific ways:

#### 4.1 Question Rows
Each question's main attributes are listed in a single row, following the column headers:
```
215,"",SingleChoiceQuestion,,,,,,,true,false,true,"Developed by...","",,true,little_interest,,false,"Over the last 2 weeks..."
```

#### 4.2 Option Rows
Each option for choice-type questions follows the parent question, with the first column blank:
```
,id,index,question_id,score,text,external_id
,910,1,215,0.0,<strong>Not at all</strong>,""
,911,2,215,1.0,<strong>Several days</strong>,""
```

#### 4.3 Validation Rows
Validations are also defined in rows following the question they belong to.

## Field Specifications

### Questionnaire Header Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Yes (for updates) | Unique identifier for the questionnaire |
| external_id | String | No | External identifier (must be alphanumeric if provided) |
| calculation_type | Enum | Yes | One of: not_applicable, summation, mean, percentage |
| route_to_after_completion | String | No | Route to redirect after completion |
| title | String | Yes | Title of the questionnaire |
| subtitle | String | No | Subtitle text |
| description | String | No | Description text |
| celebrate | Boolean | No | Whether to show celebration screen |
| celebrate_text | String | Required if celebrate=true | Text for celebration screen |
| confetti | Boolean | No | Whether to show confetti animation |
| default_language | String | Yes | Default language of the questionnaire |
| show_question | Boolean | No | Whether to show questions |
| disable_progress_bar | Boolean | No | Whether to hide progress bar |
| instructions_header | String | Required if allow_instructions=true | Instructions header text |
| instructions_back_button | String | Required if allow_instructions=true | Back button text |
| instructions_next_button | String | Required if allow_instructions=true | Next button text |
| survey_id | String | Yes | Unique identifier for the survey (must be unique) |
| new | Boolean | No | Indicates if questionnaire is new |
| allow_instructions | Boolean | No | Whether instructions are enabled |
| supported_languages | Array | Yes | List of supported languages in bracket notation |

### Question Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Yes (for updates) | Unique identifier for the question |
| external_id | String | No | External identifier (must be alphanumeric if provided) |
| type | String | Yes | Type of question (see question types below) |
| minimum | Numeric | No | Minimum value (for number/range questions) |
| maximum | Numeric | No | Maximum value (for number/range questions) |
| minimum_length | Integer | No | Minimum text length (for text questions) |
| maximum_length | Integer | No | Maximum text length (for text questions) |
| mandatory | Boolean | Yes | Whether the question is mandatory |
| confirm_skip | Boolean | No | Whether skipping requires confirmation |
| scoring | Boolean | No | Whether question has scoring |
| footer | String | No | Footer text |
| info_text | String | No | Informational text |
| description | String | Required for media questions | Description text |
| save_answer | Boolean | No | Whether to save answer |
| short_name | String | Yes (except for binah_happy_tech_questions) | Short identifier for the question |
| title | String | Yes | Question title/text |
| subtitle | String | No | Question subtitle |
| placeholder | String | No | Placeholder text for input fields |
| orientation | String | No | Layout orientation |
| data_label | String | No | Data label for reports |
| conditional_logic | JSON | No | Logic for conditional display |
| question_group_id | Integer | No | ID of the group this question belongs to |
| show_as_dropdown | Boolean | No | For choice questions, display as dropdown |
| restricted | Boolean | No | Whether question is restricted |
| routing_logic | JSON | No | Logic for routing between questions |

### Option Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Yes (for updates) | Unique identifier for the option |
| index | Integer | Yes | Display order of the option |
| question_id | Integer | Yes | ID of the parent question |
| score | Numeric | No | Score value for this option |
| text | String | Yes | Display text for the option |
| external_id | String | No | External identifier |

## Question Types

The platform supports various question types, each with specific fields and behaviors:

1. **SingleChoiceQuestion**: Single-select question with multiple options
2. **MultipleChoiceQuestion**: Multi-select question with multiple options
3. **RangeSliderQuestion**: Slider for selecting values in a range
4. **TextQuestion**: Free text input field
5. **NumberQuestion**: Numeric input field
6. **EmailQuestion**: Input field for email addresses
7. **Instruction**: Informational text (not a question)
8. **DateQuestion**: Date selection field
9. **TimeQuestion**: Time selection field
10. **DateTimeQuestion**: Combined date and time selection
11. **YearQuestion**: Year selection field
12. **PhotoQuestion**: Photo upload field
13. **VideoQuestion**: Video upload field
14. **SignatureQuestion**: Signature capture field
15. **FileUploadQuestion**: Generic file upload field
16. **BinahQuestion** and related subtypes: For biometric data
17. **HappyTechQuestion** and related subtypes: For mood/emotion tracking

## Special Features

### Calculated Variables

The CSV supports defining calculated variables using formula expressions:
```
calculated_variables,"[[[""total"", ""[PHQ9_little_interest_score] + [PHQ9_hopeless_score] + [PHQ9_sleep_score]"", ""PHQ-9 Total"", 0.0, """", """"], []]]"
```

This creates a variable named "total" that sums the scores from multiple questions, with a display name of "PHQ-9 Total" and a minimum y-axis value of 0.0.

### Question Groups

Questions can be organized into groups, defined in the question_groups row:
```
question_groups,[[1,1,"Group Title"],[2,2,"Another Group"]]
```

The format is an array of arrays, each containing [id, index, title].

### Data Points

Data points connect the questionnaire to external data:
```
data_points,"{""participant""=>[], ""survey""=>[]}"
```

## Common Import Failures

The import process can fail for various reasons:

1. **File Format Issues**:
   - Invalid CSV format
   - Non-CSV file extension
   - Incorrect MIME type
   - Missing required headers

2. **Missing Required Fields**:
   - Missing questionnaire title
   - Missing survey_id
   - Missing calculation_type
   - Missing questions (when status is published or testing)
   - Missing supported languages
   - Missing celebrate_text when celebrate is true
   - Missing instructions when allow_instructions is true

3. **Validation Failures**:
   - Duplicate survey_id
   - Invalid external_id format (must be alphanumeric)
   - Default language not in supported languages
   - No supported languages
   - Questions with invalid types
   - Missing short_name for questions (except binah/happy tech questions)
   - Missing description for photo/video questions

4. **Data Consistency Issues**:
   - Referenced question_group_id doesn't exist
   - Referenced question_id in options doesn't match parent question
   - Malformed JSON in calculated_variables, data_points, or routing_logic
   - Unsupported language not found in organization

## How IDs Work

### Question IDs

1. **In Import Mode**:
   - Existing questions: Use the ID in the CSV to match and update
   - New questions: System assigns a new ID after import
   - Questions always require a unique short_name for reference

2. **ID Mapping**:
   The import process creates mapping tables to translate between:
   - Old questionnaire ID → New questionnaire ID
   - Old question IDs → New question IDs
   - Old option IDs → New option IDs
   - Old validation IDs → New validation IDs

### Option IDs

1. **In Import Mode**:
   - Option IDs in the CSV are used for reference during import
   - They're mapped to new IDs when created in the system
   - Option index determines the display order

2. **Referencing Options**:
   - In conditional_logic, option IDs are referenced and automatically updated
   - In validations, option IDs may be referenced in the "value" field

## Import Process Flow

1. **File Upload**: User uploads a CSV file
2. **Validation**: System checks file format and basic structure
3. **Parsing**: System parses the CSV into sections:
   - Questionnaire attributes
   - Questions with their options, validations, etc.
4. **Database Creation**: In a single transaction:
   - Create or update the questionnaire
   - Create or update all questions
   - Create or update all options, validations, etc.
   - Update any references/mappings between objects
5. **Completion**: System returns the created questionnaire or error messages

## Best Practices

1. **Export First**: Before creating a new import file, export an existing questionnaire as a template
2. **Required Fields**: Always include all required fields
3. **IDs**: When updating existing questionnaires, include the correct IDs
4. **Testing**: Import to a testing environment before production
5. **Backups**: Always back up existing questionnaires before importing updates

## Example Workflow

1. Export an existing questionnaire as a CSV file
2. Modify the CSV with new questions or updates
3. Import the CSV back into the system
4. Check for any import errors
5. Verify the imported questionnaire

## Limitations

1. The import doesn't validate all dependencies at the CSV level
2. Custom formulas need to be properly formatted
3. HTML formatting in text fields must be properly escaped
4. Large questionnaires may take longer to import

## Conclusion

The WeGuide questionnaire import functionality provides a powerful way to create and update complex forms. By understanding the CSV structure and requirements, administrators can efficiently manage questionnaires without manual data entry. This technical documentation should serve as a guide for developing and using the import functionality effectively.