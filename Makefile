# Makefile for generating Marp PDF presentations

# Variables
INPUT_MD = content/slides-en.md
HEADER_MD = config/header.md
COMBINED_MD = temp/slides-en-combined.md
OUTPUT_PDF = the-zone-demo-fall-2025.pdf
TEMP_DIR = temp

# Default target
all: pdf

# Create PDF from markdown (uses Marp's built-in Chromium)
pdf: setup combine
	@echo "Building PDF..."
	marp $(COMBINED_MD) --pdf --output $(OUTPUT_PDF) --allow-local-files --pdf-outlines
	@echo "PDF built: $(OUTPUT_PDF)"

# Setup temporary directory and copy assets
setup:
	@echo "Setting up temporary directory..."
	mkdir -p $(TEMP_DIR)
	cp -r img $(TEMP_DIR)/

# Combine header and content
combine: setup
	@echo "Combining header and content..."
	cat $(HEADER_MD) $(INPUT_MD) > $(COMBINED_MD)

# Clean up generated files
clean:
	@echo "Cleaning up..."
	rm -rf $(TEMP_DIR)
	rm -f $(OUTPUT_PDF)

# Install Marp CLI
deps:
	@echo "Installing Marp CLI..."
	npm install -g @marp-team/marp-cli

# Check if Marp is installed
check-marp:
	@which marp || (echo "Marp CLI not installed. Run 'make deps' first." && exit 1)

# Preview the presentation in browser
preview: setup combine check-marp
	@echo "Starting preview server..."
	marp $(COMBINED_MD) --server --allow-local-files

# Build and open PDF
open: pdf
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(OUTPUT_PDF); \
	elif command -v open > /dev/null; then \
		open $(OUTPUT_PDF); \
	else \
		echo "Cannot open PDF automatically. Please open $(OUTPUT_PDF) manually."; \
	fi

# Help target
help:
	@echo "Available targets:"
	@echo "  all     - Build PDF (default)"
	@echo "  pdf     - Build PDF only"
	@echo "  preview - Start live preview server"
	@echo "  open    - Build PDF and open it"
	@echo "  deps    - Install Marp CLI"
	@echo "  clean   - Remove generated files"
	@echo "  help    - Show this help message"

.PHONY: all pdf setup combine clean deps preview open help check-marp
