

PYTHON ?= python3

NDK_DIR = $(HOME)/android-ndk-r25b
ANDROID_CLANGXX ?= $(NDK_DIR)/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android31-clang++
MAKEFILE_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
CXXFLAGS = -O0 -g -gdwarf-4 -ggdb3 -ffile-prefix-map=$(MAKEFILE_DIR)=. \
		-ffile-prefix-map=$(NDK_DIR)=/ndk

.PHONY: all test_binary test_binary_arm64

# Default target
all: test_binary test_binary_arm64

# Compile test binary (x86-64)
test_binary: test_binary.cpp
	clang++ $(CXXFLAGS) test_binary.cpp -o test_binary
	chmod a-x test_binary

# Compile test binary (ARM64 - requires Android NDK clang++)
test_binary_arm64: test_binary.cpp
	@if [ -f $(ANDROID_CLANGXX) ]; then \
		$(ANDROID_CLANGXX) $(CXXFLAGS) test_binary.cpp -o test_binary_arm64 && \
		chmod a-x test_binary_arm64; \
	else \
		echo "ARM64 clang++ not found at $(ANDROID_CLANGXX)." >&2; \
		exit 1; \
	fi

# Clean up bytecode and caches
clean:
	rm -rf test_binary test_binary_arm64
