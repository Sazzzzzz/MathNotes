# Makefile for LaTeX document building (cross-platform)
# cSpell: words xelatex rclone

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

.PHONY: all clean-all clean-temp list $(PROJECTS) sync merge release tag-release github-release

all: $(PROJECTS)

$(PROJECTS): %: $(OUTPUT_DIR)/%.pdf
	@$(MAKE) clean-temp

$(OUTPUT_DIR)/%.pdf: %/main.tex header.tex
	@echo Building $* PDF...
	@$(MKDIR)
	@cd $* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../$(OUTPUT_DIR) main.tex
	@cd $* && xelatex -interaction=nonstopmode -file-line-error -output-directory=../$(OUTPUT_DIR) main.tex
	@$(COPY)

list:
	@echo Available projects:
	$(LIST_CMD)
	@echo Use 'make' to build all projects
	@echo Use 'make PROJECT' to build a specific project

clean-temp:
	@$(RM_TEMP)

clean-all: clean-temp
	@$(RM_PDF)

sync: 
	rclone sync $(OUTPUT_DIR) $(SYNC_FOLDER) --verbose --size-only

merge:
	@echo "Switching to main branch..."
	@git checkout main
	@echo "Merging develop to main..."
	@git merge develop
	@echo "Merge completed successfully."
	@echo "Pushing changes to remote..."
	@git push origin main
	@echo "Changes pushed successfully."
	@echo "Switching back to develop branch..."
	@git checkout develop
	@echo "Pushing changes to remote..."
	@git push origin develop
	@echo "Changes pushed successfully."

tag-release:
	@echo "Creating tag with today's date..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "$$tag=Get-Date -Format 'yyyy-MM-dd'; echo $$tag > .release_date"; \
	else \
		date +%Y-%m-%d > .release_date; \
	fi
	@TODAY=$$(cat .release_date) && \
	git tag -a "$$TODAY" -m "Release $$TODAY" && \
	echo "Tagged version: $$TODAY" && \
	git push origin --tags && \
	echo "$$TODAY" > .current_tag
	@echo "Tag created and pushed successfully."

github-release:
	@echo "Creating GitHub release..."
	@if [ ! -f .current_tag ]; then \
		echo "No tag found. Run 'make tag-release' first."; \
		exit 1; \
	fi
	@TAG=$$(cat .current_tag) && \
	gh release create "$$TAG" $(OUTPUT_DIR)/*.pdf \
		--title "MathNotes Release $$TAG" \
		--notes-file release_message.md && \
	echo "GitHub release created successfully."
	@rm -f .current_tag .release_date

release: all merge tag-release github-release
	@echo "✅ Release process completed successfully!"
	@echo "MathNotes $(shell cat .release_date) has been released."
	@rm -f .release_date

test: tag-release
	@echo "Test complete - tag created but not published to GitHub."
	@echo "Use 'make release' for full release process."

