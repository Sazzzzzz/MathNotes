# Makefile for LaTeX document building (cross-platform)
# cSpell: words xelatex rclone

# Define colors for terminal output
RED = \033[1;31m
GREEN = \033[1;32m
YELLOW = \033[1;33m
BLUE = \033[1;34m
PURPLE = \033[1;35m
CYAN = \033[1;36m
WHITE = \033[1;37m
RESET = \033[0m

# Function to print colored messages
define colorecho
	@echo "$(1)$(2)$(RESET)"
endef

# Detect OS
ifeq ($(OS),Windows_NT)
	# Windows-specific settings
	MKDIR = if not exist $(OUTPUT_DIR) mkdir $(OUTPUT_DIR)
	COPY = copy $(OUTPUT_DIR)\main.pdf $(OUTPUT_DIR)\$*.pdf
	RM_TEMP = if exist $(OUTPUT_DIR)\*.aux del /Q $(OUTPUT_DIR)\*.aux & \
			  if exist $(OUTPUT_DIR)\*.log del /Q $(OUTPUT_DIR)\*.log & \
			  if exist $(OUTPUT_DIR)\*.out del /Q $(OUTPUT_DIR)\*.out & \
			  if exist $(OUTPUT_DIR)\*.toc del /Q $(OUTPUT_DIR)\*.toc & \
			  if exist $(OUTPUT_DIR)\*.bbl del /Q $(OUTPUT_DIR)\*.bbl & \
			  if exist $(OUTPUT_DIR)\*.blg del /Q $(OUTPUT_DIR)\*.blg & \
			  if exist $(OUTPUT_DIR)\main.pdf del /Q $(OUTPUT_DIR)\main.pdf
	RM_PDF = if exist $(OUTPUT_DIR)\*.pdf del /Q $(OUTPUT_DIR)\*.pdf
	PATH_SEP = \\
	LIST_CMD = @for %%p in ($(PROJECTS)) do @echo - %%p
else
	# macOS/Unix settings
	MKDIR = mkdir -p $(OUTPUT_DIR)
	COPY = cp $(OUTPUT_DIR)/main.pdf $(OUTPUT_DIR)/$*.pdf
	RM_TEMP = rm -f $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.out \
			  $(OUTPUT_DIR)/*.toc $(OUTPUT_DIR)/*.bbl $(OUTPUT_DIR)/*.blg \
			  $(OUTPUT_DIR)/main.pdf
	RM_PDF = rm -f $(OUTPUT_DIR)/*.pdf
	PATH_SEP = /
	LIST_CMD = @for p in $(PROJECTS); do echo "- $$p"; done
endif

# Default project list
PROJECTS = linear_algebra

# Output directory
OUTPUT_DIR = build
SYNC_FOLDER = Sync:/Sync/MathNotes_build

.PHONY: all clean-all clean-temp list $(PROJECTS) sync merge release tag-release github-release help

# Make help the default target if no target is specified
.DEFAULT_GOAL := help

all: $(PROJECTS)

$(PROJECTS): %: $(OUTPUT_DIR)/%.pdf
	@$(MAKE) clean-temp

$(OUTPUT_DIR)/%.pdf: %/main.tex header.tex
	$(call colorecho,$(BLUE),Building $* PDF...)
	@$(MKDIR)
	@cd $* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../$(OUTPUT_DIR) main.tex
	@cd $* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../$(OUTPUT_DIR) main.tex
	@$(COPY)
	$(call colorecho,$(GREEN),$* PDF built successfully!)

list:
	$(call colorecho,$(CYAN),Available projects:)
	$(LIST_CMD)
	$(call colorecho,$(CYAN),Use 'make' to build all projects)
	$(call colorecho,$(CYAN),Use 'make PROJECT' to build a specific project)

clean-temp:
	@$(RM_TEMP)

clean-all: clean-temp
	@$(RM_PDF)
	$(call colorecho,$(YELLOW),All files cleaned)

sync: 
	$(call colorecho,$(PURPLE),Syncing files to remote storage...)
	@rclone sync $(OUTPUT_DIR) $(SYNC_FOLDER) --verbose --size-only
	$(call colorecho,$(GREEN),Sync completed successfully)

merge:
	$(call colorecho,$(BLUE),Switching to main branch...)
	@git checkout main
	$(call colorecho,$(BLUE),Merging develop to main...)
	@git merge develop
	$(call colorecho,$(GREEN),Merge completed successfully.)
	$(call colorecho,$(BLUE),Pushing changes to remote...)
	@git push origin main
	$(call colorecho,$(GREEN),Changes pushed successfully.)
	$(call colorecho,$(BLUE),Switching back to develop branch...)
	@git checkout develop
	$(call colorecho,$(BLUE),Pushing changes to remote...)
	@git push origin develop
	$(call colorecho,$(GREEN),Changes pushed successfully.)

tag-release:
	$(call colorecho,$(BLUE),Creating tag with today's date...)
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "$$tag=Get-Date -Format 'yyyy-MM-dd'; echo $$tag > .release_date"; \
	else \
		date +%Y-%m-%d > .release_date; \
	fi
	@TODAY=$$(cat .release_date) && \
	git tag -a "$$TODAY" -m "Release $$TODAY" && \
	$(call colorecho,$(YELLOW),"Tagged version: $$TODAY") && \
	git push origin --tags && \
	echo "$$TODAY" > .current_tag
	$(call colorecho,$(GREEN),Tag created and pushed successfully.)

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
	$(call colorecho,$(GREEN),GitHub release created successfully.)
	@rm -f .current_tag .release_date

release: all merge tag-release github-release
	$(call colorecho,$(GREEN),✅ Release process completed successfully!)
	$(call colorecho,$(GREEN),MathNotes $$(cat .release_date) has been released.)
	@rm -f .release_date

help:
	$(call colorecho,$(CYAN),MathNotes LaTeX Build System)
	$(call colorecho,$(CYAN),============================)
	$(call colorecho,$(WHITE),Main commands:)
	$(call colorecho,$(GREEN),  make               - Build all PDF documents)
	$(call colorecho,$(GREEN),  make [project]     - Build specific project PDF)
	$(call colorecho,$(GREEN),  make list          - Show available projects)
	$(call colorecho,$(GREEN),  make clean-temp    - Remove temporary files)
	$(call colorecho,$(GREEN),  make clean-all     - Remove all generated files)
	$(call colorecho,$(WHITE),Sync commands:)
	$(call colorecho,$(GREEN),  make sync          - Sync PDFs to remote storage)
	$(call colorecho,$(WHITE),Release workflow:)
	$(call colorecho,$(GREEN),  make release       - Full release workflow (build, merge, tag, GitHub release))
	$(call colorecho,$(GREEN),  make merge         - Merge develop into main)
	$(call colorecho,$(GREEN),  make tag-release   - Create and push tag with today's date)
	$(call colorecho,$(GREEN),  make github-release - Create GitHub release with current PDFs)
