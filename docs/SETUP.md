## Set up

### Generate a new project from copier template.

```shell
copier copy https://github.com/kakaoent/alps.git <path/to/destination>
```

### Setup poetry environment for project.

```shell
cd <path/to/project>
poetry env use 3.10
poetry install
```

### Update the project from latest copier template. (if needed)

```shell
cd <path/to/project>
copier update
```

Or if you want to create a separate .rej file for each file with conflicts.

```shell
copier update --conflict rej
```

These files contain the unresolved diffs.

make sure `git status` shows it clean
