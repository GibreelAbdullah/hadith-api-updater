##This repo and hadith-api repo should have the same parent directory.

This repo is used to add new functionality to the hadith-api repo.

in hadith-api

```bash
git checkout 2
git reset --hard origin/1
```
- in case there are new books added run below script to update editions.json

  - put new book txt in start folder and then
  - ```bash
    node apiscript.js update
    ```

run 

```bash
run.sh
```

update apiscript.js to change `process.env.CI` to `true`.

copy all files from `database/line-by-line` and put in `start` folder.

run 

```bash
node apiscript.js update
```