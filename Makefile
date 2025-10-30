VENV=.venv
PY=$(VENV)/bin/python

.PHONY: venv substack-login substack-publish nb2md

venv:
	python -m venv $(VENV)
	. $(VENV)/bin/activate; pip install -r requirements-substack.txt; python -m playwright install

substack-login: venv
	$(PY) tools/substack/cli.py login

# use: make substack-publish FILE=docs/my.md PUBLISH=true
substack-publish: venv
	$(PY) tools/substack/cli.py publish $(FILE) $(if $(PUBLISH),--publish,)

# Example: make nb2md NB=notebooks/demo.ipynb OUT=docs/demo.md TITLE="Demo" TAGS="eval,release"
nb2md: venv
	$(PY) scripts/export_notebook.py --in $(NB) --out $(OUT) --title "$(TITLE)" --tags "$(TAGS)"
