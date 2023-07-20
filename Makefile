configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./profcomff_parse_lib
	isort ./profcomff_parse_lib
	black ./profcomff_parse_lib