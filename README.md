# blaise-editing-cloud-functions
This cloud functions if used to send cases from the "main" (interviewer) dataset to the "edit" (editor) dataset.
This is required for the [Blaise Editing Service](https://github.com/ONSdigital/blaise-editing-service). 

## Service functionality

This project contain one service which is a cloud function called ``copy-cases-to-edit``.

``copy-cases-to-edit`` takes in a parameter called ``survey_type``, this will then run the service for all questionnaires installed which start with the input you give it. So for example:
* if the service is given a survey name ("FRS" for example) it will run for all questionnaires installed for FRS
* if the service is given a questionnaire name ("FRS2504A" for example) it will only run for that questionnaire

It then checks that both "main" and "edit" have been installed for the questionnaire.
If they are it will copy over cases from "main" to "edit" overwriting them if they already exist.

All cases are copied unless editing has already begun in the "edit" questionnaire for the case.
This is identified in the "edit" questionnaire by the field **``QEdit.Edited``**.
If ``QEdit.Edited`` is set to '1' then editing has begun and the case is not overwritten.


## Required Questionnaires

For this service to be able to copy between the questionnaire's datasets they must both be installed first:

### "Main" questionnaire

The "main" questionnaire, which the interviewers complete is completed the same way as the other surveys.

### "Edit" questionnaire

The "edit" questionnaire, is the same as the "main" questionnaire but makes use of the edit block.
It needs to be named the same as the "main" questionnaire but with ``_EDIT`` on the end.



## Local Setup

The service cannot be run locally, you cannot locally connect to the SQL instance as Public IP connectivity is disabled.  To run this cloud function you need to deploy to a sandbox where you can run it there.


To be able to run the tests locally run the following:

Clone the project locally:
```shell
git clone https://github.com/ONSdigital/blaise-editing-cloud-functions.git
```

Install poetry:
```shell
pip install poetry
```

Install dependencies:
```shell
poetry install --no-root
```

Before pushing code up make sure all the following passes:

Run MyPy to check types:
```shell
poetry run mypy .
```

Run black to run linting:
```shell
poetry run black .
```

Run unit tests:
```shell
poetry run python -m pytest
```
