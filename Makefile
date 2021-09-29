LIB_DIR=lib/$(NAME)
STACK_DIR=stacks/$(NAME)
TEMPLATE_DIR?=stack
PY_VERSION:=$(shell cat .python-version)
TF_VERSION:=$(shell cat .terraform-version)
VENV_NAME:="$(NAME)-$(PY_VERSION)"

library:
	cp -R templates/library $(LIB_DIR)
	mv $(LIB_DIR)/example_library $(LIB_DIR)/$(NAME)
	sed -i.tmp 's/library-template/$(NAME)/' $(LIB_DIR)/setup.py
	rm $(LIB_DIR)/setup.py.tmp

init:
	@if [ -d $(STACK_DIR) ]; then echo 'Stack "$(NAME)" already exists'; exit 1; fi
	tfenv use $(TF_VERSION)
	pyenv uninstall -f $(VENV_NAME)
	pyenv virtualenv $(PY_VERSION) $(VENV_NAME)
	cp -R templates/$(TEMPLATE_DIR) $(STACK_DIR)
	sed -i.tmp 's/Example\ stack/$(NAME)/' $(STACK_DIR)/main.py
	sed -i.tmp 's/example-stack/$(NAME)/' $(STACK_DIR)/main.py
	rm $(STACK_DIR)/main.py.tmp
	echo $(VENV_NAME) > $(STACK_DIR)/.python-version
