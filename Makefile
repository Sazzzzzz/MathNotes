# Makefile for LaTeX document building on Windows
# cSpell: words xelatex rclone
# Default project list
# TODO: Add error handling
PROJECTS = linear_algebra math_formulas

# Output directory
OUTPUT_DIR = build
SYNC_FOLDER = Sync:/Sync/MathNotes_build

.PHONY: all clean-all clean-temp list $(PROJECTS) sync

# Main build command - build all projects
all: $(PROJECTS) sync

# Make each project depend on its PDF output
$(PROJECTS): %: $(OUTPUT_DIR)/%.pdf
	@$(MAKE) clean-temp

# Define dependencies for each project
define project_deps
$(OUTPUT_DIR)/$(1).pdf: header.tex $$(wildcard $(1)/*.tex)
	@echo Building $(1) PDF...
	@if not exist $(OUTPUT_DIR) mkdir $(OUTPUT_DIR)
	xelatex -include-directory=./$(1) -interaction=nonstopmode -file-line-error -output-directory=$(OUTPUT_DIR) $(1)/main.tex
	xelatex -include-directory=./$(1) -interaction=nonstopmode -file-line-error -output-directory=$(OUTPUT_DIR) $(1)/main.tex
	@copy $(OUTPUT_DIR)\main.pdf $(OUTPUT_DIR)\$(1).pdf
endef

# Generate specific rules for each project with all its .tex files as dependencies
$(foreach proj,$(PROJECTS),$(eval $(call project_deps,$(proj))))

# List available projects
list:
	@echo Available projects:
	@for %%p in ($(PROJECTS)) do @echo - %%p
	@echo Use 'make' to build all projects
	@echo Use 'make PROJECT' to build a specific project

# Clean up temporary files but keep PDFs
clean-temp:
	@if exist $(OUTPUT_DIR)\*.aux del /Q $(OUTPUT_DIR)\*.aux
	@if exist $(OUTPUT_DIR)\*.log del /Q $(OUTPUT_DIR)\*.log
	@if exist $(OUTPUT_DIR)\*.out del /Q $(OUTPUT_DIR)\*.out
	@if exist $(OUTPUT_DIR)\*.toc del /Q $(OUTPUT_DIR)\*.toc
	@if exist $(OUTPUT_DIR)\*.bbl del /Q $(OUTPUT_DIR)\*.bbl
	@if exist $(OUTPUT_DIR)\*.blg del /Q $(OUTPUT_DIR)\*.blg
	@if exist $(OUTPUT_DIR)\main.pdf del /Q $(OUTPUT_DIR)\main.pdf

# Clean everything including PDFs
clean-all: clean-temp
	@if exist $(OUTPUT_DIR)\*.pdf del /Q $(OUTPUT_DIR)\*.pdf

sync: 
	rclone sync $(OUTPUT_DIR) $(SYNC_FOLDER) --verbose --size-only