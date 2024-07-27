# Hadith Search Api 2.0

This service provides the Search functionality in the website [HadithHub](https://www.hadithhub.com/), which provides Ahadith in multiple languages and grades.

This is an update to [hadith-search-api](https://github.com/GibreelAbdullah/hadith-search-api), it is designed to be hosted on AWS Lambda but can be used on any service with minor tweaks.

## Architecture

The architecture of this search service revolves around a "controller" Lambda function and multiple worker Lambda functions. Each worker Lambda is responsible for handling searches for a specific book and its translations. Here's a step-by-step explanation of the setup:

1. Controller Lambda Function (controller.py):

    The controller Lambda function receives the initial search query from the user.
It then triggers the worker Lambda functions in parallel, each in a separate thread, to perform the actual search.
Once the worker Lambdas return their results, the controller function aggregates these results based on their matching scores and returns the final compiled results to the user.

2. Worker Lambda Functions (app.py):

    Each worker Lambda is assigned a specific book and its translations.
These functions have an embedded SQLite database containing the text of the assigned book and translations.
Upon receiving the search query from the controller Lambda, the worker Lambda searches within its database for relevant matches and calculates a matching score for each result.
The results, along with their scores, are then sent back to the controller Lambda.

## Important Script Functions

1. controller.py - The controller lambda function which receives the initial request and triggers relevant worker lambdas, get their responses, combines them into one and reutrn the consolidated result.

2. app.py - The worker lambda function. This is included in each worker lambda (one for each book and transalation). It searches the database of that specific lambda function and returns the response along with a matching score to the controller lambda.

3. 01-CreateDatabases.py - Python script to create multiple databases (one for each book and transalation). It uses the data from [hadith-api](https://github.com/GibreelAbdullah/hadith-api/).

4. 02-ZipAndDeployWorkerLambdas.sh - Bash script to deploy all the worker lambdas. It Zips hadith.db, app.py and query.py which is then deployed to AWS lambda

5. 03-ZipAndDeployControllerLambda.sh - Bash script to deploy controller lambda. It Zips controller.py which is then deployed to AWS lambda