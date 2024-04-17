# Alps

AI Lab Pipeline Starter

![Python](https://img.shields.io/pypi/pyversions/alps?logo=python&logoColor=%2523959DA5)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

```
⠀⠀⠀⠀⠀⠀⠀⣠⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⠟⣿⣷⡀⠀⢀⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⠟⠀⠈⣿⣷⣰⣿⡿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣰⣿⡏⠀⠀⠀⠘⣿⣿⡟⠀⠹⣿⣦⠀⣴⣾⣶⡀⠀⠀⠀
⠀⠀⠀⣰⣿⣿⣶⣿⣿⣄⠀⠈⠋⠀⠀⠀⠹⣿⣾⣿⠟⣿⣷⠀⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⢀⣴⣶⣄⡹⣿⣇⠀⠘⣿⣧⠀⠀
⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣆⠀

    _____  .__                 
   /  _  \ |  | ______  ______ 
  /  /_\  \|  | \____ \/  ___/ 
 /    |    \  |_|  |_> >___ \  
 \____|__  /____/   __/____  > 
         \/     |__|       \/  
```

## Prerequisites

[Prerequisites](docs/PREREQUISITES.md)

## Setup a project

[Setup a project](docs/SETUP.md)

## Usage

### Create a component.

```shell
./alps.sh create component <component-name>
```

### Create a pipeline.

```shell
./alps.sh create pipeline <pipeline-name>
```

### Build containerized components.

(If you have components that need to be containerized.)

```shell
./alps.sh build components
```

### Compile pipelines.

```shell
./alps.sh compile pipelines
```

### Upload containerized components to the Artifact Registry.

```shell
./alps.sh upload components
```

### Upload pipelines to the Vertex AI Pipelines.

```shell
./alps.sh upload pipelines
```

### Add the repository to a workload identity pool.

(to access Google Cloud resources from the GitHub Actions
Run this command only once for each repository.)

```shell
./alps.sh configure wipr <repository-name>
```

### Add required packages.

```shell
poetry add <package>
```

## Additional scripts

### Train model for test.

```shell
./scripts/sample/train.sh
```

### Submit the job to run the pipeline.

```shell
./scripts/sample/submit.sh
```
