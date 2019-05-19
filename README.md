# Clickupy

A library and CLI for interacting with [Clickup](https://clickup.com)

## Getting Started

To install the library run `pip3 install clickupy`

## Usage

```
$ clickup --help
Usage: clickup [OPTIONS] COMMAND [ARGS]...

  A command line tool for interacting with clickup

Options:
  --format [human|json]
  --api_key TEXT         An API KEY for clickup  [required]
  --help                 Show this message and exit.

Commands:
  fuse      Create a FUSE filesystem for Clickup resources
  projects  Get a space's projects
  spaces    Get a team's spaces
  tasks     Get a team's spaces
  team      Get a user's team
  teams     Get a user's teams
  user      Get a user
```

## Fuse

The fuse subcommand has only been tested on OSX. To enable FUSE on OSX, install [OSXFUSE](https://osxfuse.github.io/).

## License

This project is licensed under the MIT License.
