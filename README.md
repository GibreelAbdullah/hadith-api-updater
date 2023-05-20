##This repo and hadith-api repo should have the same parent directory.

This repo is used to add new functionality to the hadith-api repo.

```bash
git checkout 2
git reset --hard origin/1
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