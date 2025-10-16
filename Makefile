# Makefile for LaTeX document building (cross-platform)
# cSpell: words xelatex rclone

#==============================================================================
# Configuration
#==============================================================================

# Project structure
NOTES_DIR = notes
OUTPUT_DIR = build
SYNC_FOLDER = Sync:/Sync/MathNotes

# Project definitions
ALL_PROJECTS = linear_algebra real_analysis geometry probability mathematical_analysis optimization_method math_formulas mathematical_physics_equations functional_analysis
PROJECTS = linear_algebra real_analysis geometry probability functional_analysis

# Color definitions for terminal output
COLORS = RED=\033[1;31m GREEN=\033[1;32m YELLOW=\033[1;33m BLUE=\033[1;34m PURPLE=\033[1;35m CYAN=\033[1;36m WHITE=\033[1;37m RESET=\033[0m
$(foreach color,$(COLORS),$(eval $(color)))

#==============================================================================
# Platform Detection & Commands
#==============================================================================

ifeq ($(OS),Windows_NT)
    # Windows commands
    MKDIR = if not exist $(OUTPUT_DIR) mkdir $(OUTPUT_DIR)
    COPY = copy $(OUTPUT_DIR)\main.pdf $(OUTPUT_DIR)\$*.pdf
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
    COPY = cp $(OUTPUT_DIR)/main.pdf $(OUTPUT_DIR)/$*.pdf
    CLEAN_TEMP_FILES = rm -f $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.out \
                       $(OUTPUT_DIR)/*.toc $(OUTPUT_DIR)/*.bbl $(OUTPUT_DIR)/*.blg \
                       $(OUTPUT_DIR)/*.bcf $(OUTPUT_DIR)/*.run.xml $(OUTPUT_DIR)/main.pdf
    CLEAN_PDFS = rm -f $(OUTPUT_DIR)/*.pdf
    LIST_PROJECTS = @for p in $(1); do echo "- $$p"; done
    colorecho = @printf "$(1)$(2)$(RESET)\n"
endif

#==============================================================================
# Functions
#==============================================================================

# Get all .tex files for a specific project
get_tex_files = $(wildcard $(NOTES_DIR)/$(1)/*.tex)

# Get all source files, excluding _temp directories
ALL_SOURCE_FILES = $(shell find $(NOTES_DIR) -type d -name '*_temp' -prune -o -type f -print)

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

.PHONY: all build-all clean-all clean-temp list list-all sync merge release tag-release github-release help $(ALL_PROJECTS)
.DEFAULT_GOAL := help

# Build targets
all: $(PROJECTS)

build-all: $(ALL_PROJECTS)

$(ALL_PROJECTS): %: $(OUTPUT_DIR)/%.pdf
	@$(MAKE) clean-temp

# PDF generation rule
$(OUTPUT_DIR)/%.pdf: $(ALL_SOURCE_FILES)
	$(call colorecho,$(BLUE),Building $* PDF...)
	@$(MKDIR)
	@cd $(NOTES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@cd $(NOTES_DIR)/$* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../../$(OUTPUT_DIR) main.tex
	@$(COPY)
	$(call colorecho,$(GREEN),$* PDF built successfully!)

# Add dependencies for all .tex files in each project
# $(foreach proj,$(ALL_PROJECTS),$(eval $(OUTPUT_DIR)/$(proj).pdf: $(call get_tex_files,$(proj))))

# Information targets
list:
	$(call colorecho,$(CYAN),Default LaTeX projects (built by 'make all'):)
	$(call LIST_PROJECTS,$(PROJECTS))
	$(call colorecho,$(CYAN),Use 'make' to build default projects or 'make PROJECT' for specific project)

list-all:
	$(call colorecho,$(CYAN),All available LaTeX projects:)
	$(call LIST_PROJECTS,$(ALL_PROJECTS))
	$(call colorecho,$(CYAN),Use 'make build-all' to build all projects)

# Cleanup targets
clean-temp:
	@$(CLEAN_TEMP_FILES)

clean-all: clean-temp
	@$(CLEAN_PDFS)
	$(call colorecho,$(YELLOW),All files cleaned)

# Sync target
sync: 
	$(call colorecho,$(PURPLE),Syncing files to remote storage...)
	@rclone sync $(OUTPUT_DIR) $(SYNC_FOLDER) --verbose --size-only
	$(call colorecho,$(GREEN),Sync completed successfully)

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
	$(call colorecho,$(GREEN),  make / make all    - Build default projects: $(PROJECTS))
	$(call colorecho,$(GREEN),  make build-all     - Build all projects: $(ALL_PROJECTS))
	$(call colorecho,$(GREEN),  make <project>     - Build specific project)
	$(call colorecho,$(WHITE),Information:)
	$(call colorecho,$(GREEN),  make list          - Show default projects)
	$(call colorecho,$(GREEN),  make list-all      - Show all available projects)
	$(call colorecho,$(WHITE),Maintenance:)
	$(call colorecho,$(GREEN),  make clean-temp    - Remove temporary build files)
	$(call colorecho,$(GREEN),  make clean-all     - Remove all generated files)
	$(call colorecho,$(GREEN),  make sync          - Sync PDFs to remote storage)
	$(call colorecho,$(WHITE),Release Workflow:)
	$(call colorecho,$(GREEN),  make release       - Complete release: build + merge + tag + GitHub release)
	$(call colorecho,$(GREEN),  make merge         - Merge develop→main and push)
	$(call colorecho,$(GREEN),  make tag-release   - Create date-based tag)
	$(call colorecho,$(GREEN),  make github-release - Create GitHub release)
	$(call colorecho,$(GREEN),  make clean-temp    - Remove temporary files)
	$(call colorecho,$(GREEN),  make clean-all     - Remove all generated files)
	$(call colorecho,$(WHITE),Sync commands:)
	$(call colorecho,$(GREEN),  make sync          - Sync PDFs to remote storage)
	$(call colorecho,$(WHITE),Release workflow:)
	$(call colorecho,$(GREEN),  make release       - Full release workflow (build, merge, tag, GitHub release))
	$(call colorecho,$(GREEN),  make merge         - Merge develop into main)
	$(call colorecho,$(GREEN),  make tag-release   - Create and push tag with today's date)
	$(call colorecho,$(GREEN),  make github-release - Create GitHub release with current PDFs)
