.PHONY: serve clean

serve:
	python run.py --development

clean:
	rm -rf app/static/users/sample_username/*
