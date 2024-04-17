## Prerequisites

### Install pyenv. (Optional)

```shell
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

### Install python 3.10.x with pyenv. (Optional)

```shell
pyenv install 3.10
pyenv global 3.10
```

### Install pipx.

link: [Install pipx](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx, "install pipx link")

### Install poetry.

```shell
pipx install poetry
```

### Install copier.

```shell
pipx install copier
```
