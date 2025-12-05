# Makefile for LaTeX document building (cross-platform)
# cSpell: words xelatex

#==============================================================================
# Configuration
#==============================================================================

# Project structure
NOTES_DIR = notes
ARTICLES_DIR = articles
OUTPUT_DIR = build

# Project definitions - separate lists for notes and articles
NOTES_PROJECTS = linear_algebra real_analysis geometry probability functional_analysis
ARTICLES_PROJECTS = simplex_method

# Combined project lists with prefixes for build targets
ALL_NOTES = $(addprefix notes-,$(NOTES_PROJECTS))
ALL_ARTICLES = $(addprefix articles-,$(ARTICLES_PROJECTS))
ALL_PROJECTS = $(ALL_NOTES) $(ALL_ARTICLES)

# Default projects to build (all notes and articles)
PROJECTS = $(ALL_PROJECTS)

# Color definitions for terminal output
COLORS = RED=\033[1;31m GREEN=\033[1;32m YELLOW=\033[1;33m BLUE=\033[1;34m PURPLE=\033[1;35m CYAN=\033[1;36m WHITE=\033[1;37m RESET=\033[0m
$(foreach color,$(COLORS),$(eval $(color)))

#==============================================================================
# Platform Detection & Commands
#==============================================================================

ifeq ($(OS),Windows_NT)
	# Windows commands
	MKDIR = if not exist $(OUTPUT_DIR) mkdir $(OUTPUT_DIR)
	CLEAN_TEMP_FILES = if exist $(OUTPUT_DIR)\*.aux del /Q $(OUTPUT_DIR)\*.aux & \
					   if exist $(OUTPUT_DIR)\*.log del /Q $(OUTPUT_DIR)\*.log & \
					   if exist $(OUTPUT_DIR)\*.out del /Q $(OUTPUT_DIR)\*.out & \
					   if exist $(OUTPUT_DIR)\*.toc del /Q $(OUTPUT_DIR)\*.toc & \
					   if exist $(OUTPUT_DIR)\*.bbl del /Q $(OUTPUT_DIR)\*.bbl & \
					   if exist $(OUTPUT_DIR)\*.blg del /Q $(OUTPUT_DIR)\*.blg & \
					   if exist $(OUTPUT_DIR)\*.bcf del /Q $(OUTPUT_DIR)\*.bcf & \
					   if exist $(OUTPUT_DIR)\*.run.xml del /Q $(OUTPUT_DIR)\*.run.xml & \
					   if exist $(OUTPUT_DIR)\main.pdf del /Q $(OUTPUT_DIR)\main.pdf
	CLEAN_PDFS = if exist $(OUTPUT_DIR)\*.pdf del /Q $(OUTPUT_DIR)\*.pdf
	LIST_PROJECTS = @for %%p in ($(1)) do @echo - %%p
	colorecho = @echo $(2)
else
	# Unix/macOS commands
	MKDIR = mkdir -p $(OUTPUT_DIR)
	CLEAN_TEMP_FILES = rm -f $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.out \
					   $(OUTPUT_DIR)/*.toc $(OUTPUT_DIR)/*.bbl $(OUTPUT_DIR)/*.blg \
					   $(OUTPUT_DIR)/*.bcf $(OUTPUT_DIR)/*.run.xml \
					   $(OUTPUT_DIR)/main.pdf
	CLEAN_PDFS = rm -f $(OUTPUT_DIR)/*.pdf
	LIST_PROJECTS = @for p in $(1); do echo "  - $$p"; done
	colorecho = @printf "$(1)$(2)$(RESET)\n"
endif

#==============================================================================
# Functions
#==============================================================================

# Get all source files from both directories, excluding _temp directories
ALL_SOURCE_FILES = $(shell find $(NOTES_DIR) $(ARTICLES_DIR) -type d -name '*_temp' -prune -o -type f -print 2>/dev/null)

# Create date tag for releases
define create_date_tag
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "$$tag=Get-Date -Format 'yyyy-MM-dd'; echo $$tag > .release_date"; \
	else \
		date +%Y-%m-%d > .release_date; \
	fi
endef

#==============================================================================
# Targets
#==============================================================================

.PHONY: all build-all clean-all clean-temp list list-all merge release tag-release github-release help $(ALL_PROJECTS)
.DEFAULT_GOAL := help

# Build targets
all: $(PROJECTS)

build-all: $(ALL_PROJECTS)

# Notes build rule: notes-<project> -> build/notes-<project>.pdf
$(ALL_NOTES): notes-%: $(OUTPUT_DIR)/notes-%.pdf
	@$(MAKE) --no-print-directory clean-temp

$(OUTPUT_DIR)/notes-%.pdf: $(ALL_SOURCE_FILES)
	$(call colorecho,$(BLUE),Building notes: $* ...)
	@$(MKDIR)
	@cd $(NOTES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@cd $(NOTES_DIR)/$* && biber --output-directory ../../$(OUTPUT_DIR) main
	@cd $(NOTES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@cd $(NOTES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@mv $(OUTPUT_DIR)/main.pdf $(OUTPUT_DIR)/notes-$*.pdf
	$(call colorecho,$(GREEN),notes-$*.pdf built successfully!)

# Articles build rule: articles-<project> -> build/articles-<project>.pdf
$(ALL_ARTICLES): articles-%: $(OUTPUT_DIR)/articles-%.pdf
	@$(MAKE) --no-print-directory clean-temp

$(OUTPUT_DIR)/articles-%.pdf: $(ALL_SOURCE_FILES)
	$(call colorecho,$(BLUE),Building article: $* ...)
	@$(MKDIR)
	@cd $(ARTICLES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@cd $(ARTICLES_DIR)/$* && biber --output-directory ../../$(OUTPUT_DIR) main
	@cd $(ARTICLES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@cd $(ARTICLES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@mv $(OUTPUT_DIR)/main.pdf $(OUTPUT_DIR)/articles-$*.pdf
	$(call colorecho,$(GREEN),articles-$*.pdf built successfully!)

# Information targets
list:
	$(call colorecho,$(CYAN),Default LaTeX projects (built by 'make all'):)
	$(call colorecho,$(WHITE),Notes:)
	$(call LIST_PROJECTS,$(NOTES_PROJECTS))
	$(call colorecho,$(WHITE),Articles:)
	$(call LIST_PROJECTS,$(ARTICLES_PROJECTS))

list-all:
	$(call colorecho,$(CYAN),All available LaTeX projects:)
	$(call colorecho,$(WHITE),Notes (prefix: notes-):)
	$(call LIST_PROJECTS,$(NOTES_PROJECTS))
	$(call colorecho,$(WHITE),Articles (prefix: articles-):)
	$(call LIST_PROJECTS,$(ARTICLES_PROJECTS))
	$(call colorecho,$(CYAN),Use 'make notes-<name>' or 'make articles-<name>' to build specific project)

# Cleanup targets
clean-temp:
	@$(CLEAN_TEMP_FILES)

clean-all: clean-temp
	@$(CLEAN_PDFS)
	$(call colorecho,$(YELLOW),All files cleaned)

# Git workflow targets
merge:
	$(call colorecho,$(BLUE),Merging develop to main and pushing...)
	@git checkout main && git merge develop && git push origin main
	@git checkout develop && git push origin develop
	$(call colorecho,$(GREEN),Merge workflow completed successfully)

tag-release:
	$(call colorecho,$(BLUE),Creating tag with today's date...)
	$(call create_date_tag)
	@TODAY=$$(cat .release_date) && \
	git tag -a "$$TODAY" -m "Release $$TODAY" && \
	git push origin --tags && \
	echo "$$TODAY" > .current_tag
	$(call colorecho,$(GREEN),Tag created and pushed successfully)

github-release:
	$(call colorecho,$(BLUE),Creating GitHub release...)
	@if [ ! -f .current_tag ]; then \
		$(call colorecho,$(RED),No tag found. Run 'make tag-release' first.); \
		exit 1; \
	fi
	@TAG=$$(cat .current_tag) && \
	gh release create "$$TAG" $(OUTPUT_DIR)/*.pdf \
		--title "MathNotes Release $$TAG" \
		--notes-file release_message.md && \
	rm -f .current_tag .release_date
	$(call colorecho,$(GREEN),GitHub release created successfully)

release: all merge tag-release github-release
	$(call colorecho,$(GREEN),✅ Release process completed successfully!)

# Help target
help:
	$(call colorecho,$(CYAN),MathNotes LaTeX Build System)
	$(call colorecho,$(CYAN),============================)
	$(call colorecho,$(WHITE),Build Commands:)
	$(call colorecho,$(GREEN),  make all			 - Build all notes and articles)
	$(call colorecho,$(GREEN),  make notes-<name>	- Build specific note (e.g. make notes-geometry))
	$(call colorecho,$(GREEN),  make articles-<name> - Build specific article (e.g. make articles-math_formulas))
	$(call colorecho,$(WHITE),Information:)
	$(call colorecho,$(GREEN),  make list			- Show default projects)
	$(call colorecho,$(GREEN),  make list-all		- Show all available projects with usage)
	$(call colorecho,$(WHITE),Maintenance:)
	$(call colorecho,$(GREEN),  make clean-temp	  - Remove temporary build files)
	$(call colorecho,$(GREEN),  make clean-all	   - Remove all generated files)
	$(call colorecho,$(WHITE),Release Workflow:)
	$(call colorecho,$(GREEN),  make release		 - Complete release: build + merge + tag + GitHub release)
	$(call colorecho,$(GREEN),  make merge		   - Merge develop→main and push)
	$(call colorecho,$(GREEN),  make tag-release	 - Create date-based tag)
	$(call colorecho,$(GREEN),  make github-release  - Create GitHub release with PDFs)