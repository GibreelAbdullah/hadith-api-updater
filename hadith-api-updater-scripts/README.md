# HADITH API UPDATER SCRIPTS

This folder contains the script which generates the data in the [hadith-api-master](https://github.com/GibreelAbdullah/hadith-api-updater/tree/master/hadith-api-master) folder.

The scripts are triggered on every push by GithubActions.

The GithubActions

1. Pulls all the relevant data from [hadith-api by fawazahmed0](https://github.com/fawazahmed0/hadith-api/).
2. Runs the scripts to add additional data (Like some books that are not there in upstream repo, details of muhaddith etc.). Not all the scripts preset are executed. Some are not needed.
3. All the changes are added to [hadith-api-master](https://github.com/GibreelAbdullah/hadith-api-updater/tree/master/hadith-api-master) folder.
4. Creates the database needed for search service.
5. Deploys the search service to AWS Lambda.