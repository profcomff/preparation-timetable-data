configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./profcomff_parse_lib
	source ./venv/bin/activate && isort ./profcomff_parse_lib
	source ./venv/bin/activate && black ./profcomff_parse_lib
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./tests
	source ./venv/bin/activate && isort ./tests
	source ./venv/bin/activate && black ./tests
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./migrations
	source ./venv/bin/activate && isort ./migrations
	source ./venv/bin/activate && black ./migrations

run-main:
	source ./venv/bin/activate && python3 main.py

run-autoupdate:
	source ./venv/bin/activate && python3 autoupdate.py