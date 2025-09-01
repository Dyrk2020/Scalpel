
PYTHON ?= python3

.PHONY: all build test install clean

# Default target
all: build test

# Build the proxy
build:
	$(PYTHON) install.py build

# Run unit tests
test:
	$(PYTHON) install.py test

# Install the plugin loader to IDA
install:
	$(PYTHON) install.py plugin

gemini:
	$(PYTHON) install.py gemini

# Clean up bytecode and caches
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
