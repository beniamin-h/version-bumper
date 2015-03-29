# version-bumper
App.yaml based version bumper

### Usage:

```
./bump.py [-h] [-c] {major,minor,maintenance}

positional arguments:
  {major,minor,maintenance}
                        Change significance

optional arguments:     
  -h, --help            Show help message and exit
  -c, --commit          Commit version bump to local git repository
```

### Requirements

* Python3 (tested with Python3.4)

### Key features

* Changes any number-based version (eg. 12, 4.2, 5.081.3)    
to format x.y.z (major, minor, maintenance)
* Optionally commits version bump to local git repository
* Preserves present config items order
* Sequences (lists) indenting
* Works with any valid yaml file

### Advanced usage

For shorthand you can use your shell aliases, eg.:

`cp bump.py /opt/bump.py`    
`alias bump-major='/opt/bump.py major'`    
`alias bump-minor='/opt/bump.py minor'`     
`alias bump-maintenance='/opt/bump.py maintenance'`     

In order to avoid to type this on every login it's recommended to put aliases into your shell runcom file (like ~/.bashrc, ~/.zshrc etc.).

