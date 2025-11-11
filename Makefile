# Makefile for generating Marp PDF presentations

# Variables
INPUT_MD = content/slides-en.md
HEADER_MD = config/header.md
COMBINED_MD = temp/slides-en-combined.md
OUTPUT_PDF = the-zone-demo-fall-2025.pdf
TEMP_DIR = temp

# Default target
all: pdf

# Create PDF from markdown using Chrome
pdf: setup combine
	@echo "Building PDF with Chrome..."
	PUPPETEER_PRODUCT=chrome marp $(COMBINED_MD) --pdf --output $(OUTPUT_PDF) --allow-local-files --pdf-outlines
	@echo "PDF built: $(OUTPUT_PDF)"

# Alternative: Explicitly specify Chrome path if needed
pdf-chrome: setup combine
	@echo "Building PDF with explicit Chrome path..."
	CHROME_PATH=/usr/bin/google-chrome marp $(COMBINED_MD) --pdf --output $(OUTPUT_PDF) --allow-local-files --pdf-outlines
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

# Install only Marp CLI
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

# Find Chrome path (for debugging)
chrome-path:
	@echo "Finding Chrome installation..."
	@which google-chrome || which chromium-browser || echo "Chrome/Chromium not found in PATH"

# Help target
help:
	@echo "Available targets:"
	@echo "  all         - Build PDF (default)"
	@echo "  pdf         - Build PDF using Chrome"
	@echo "  pdf-chrome  - Build PDF with explicit Chrome path"
	@echo "  preview     - Start live preview server"
	@echo "  open        - Build PDF and open it"
	@echo "  deps        - Install Marp CLI only"
	@echo "  chrome-path - Show Chrome installation path"
	@echo "  clean       - Remove generated files"
	@echo "  help        - Show this help message"

.PHONY: all pdf pdf-chrome setup combine clean deps preview open chrome-path help check-marp
