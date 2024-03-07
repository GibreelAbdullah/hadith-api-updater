##This repo and hadith-api repo should have the same parent directory.

This repo is used to add new functionality to the hadith-api repo.

Follow the steps below.

1. In `hadith-api` reset to the latest origin `git reset --hard origin/1`
2. Make the relevant changes. Will have to update `info.json` and hadith text file which should be placed in `start` folder.
3. Push the changes to github.
4. Run the github action named `CI` using `update` or `create` command.
5. Once completed pull the changes to local.
6. run `./run.sh` to update the data in `hadith-api` with extra info.
7. run `./run2.sh` to copy the changes from `hadith-api` to `hadith-api-master` which is just `hadith-api` but on branch `2` which is used by `HadithHub`