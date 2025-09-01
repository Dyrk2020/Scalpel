# How to contribute

We'd love to accept your patches and contributions to this project!

## Submitting changes

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Development and Testing Workflow

When contributing code changes, please make sure your changes align with the
project architecture and pass our existing tests:

1.  **Build and Test**: Run `make test` from the root directory to run unit
    tests and ensure your changes do not introduce regressions. If you modify
    core tool definitions or proxy routing, run `make build`.
2.  **Code Style**: Ensure Python code adheres to PEP 8 standards, uses type
    annotations (compatible with Python 3.10+), and includes descriptive
    docstrings.
3.  **Pull Requests**: Open a GitHub Pull Request with a clear summary of what
    your change does and any relevant context or testing steps.
