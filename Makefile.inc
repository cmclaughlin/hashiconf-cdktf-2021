VENV_NAME:=$(shell cat .python-version)
VENV:=~/.pyenv/versions/$(VENV_NAME)/bin/activate
PY_VERSION:=$(shell cat ../../.python-version)

.PHONY: init
init:
	pyenv virtualenv -f $(PY_VERSION) $(VENV_NAME)
	echo "Run this to activate the env"
	echo "pyenv activate $(VENV_NAME)"


.PHONY: install
install:
	. $(VENV) && pip install --upgrade pip
	. $(VENV) && pip install -r requirements.txt
	../../scripts/generate_providers.sh

.PHONY: clean
clean:
	rm -rf cdktf.out .terraform/terraform.tfstate

.PHONY: synth
synth:
	ENV=$(ENV) python main.py

.PHONY: apply
apply: STACK_DIR=$(shell ls cdktf.out/stacks)
apply: STACK_DIR_PATH=cdktf.out/stacks/$(STACK_DIR)
apply:
	cd $(STACK_DIR_PATH) && echo "no" | terraform init
	cd $(STACK_DIR_PATH) && terraform apply

.PHONY: ops
ops: ENV=ops
ops: clean synth apply
