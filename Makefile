.PHONY: build check preview release clean
build:
	python3 scripts/build.py
check: build
	python3 scripts/check_publications.py
	python3 scripts/check_locales.py
	python3 scripts/check.py
	python3 scripts/check_ar_pilot.py
	python3 scripts/check_ar_advisory.py
preview: build
	python3 scripts/serve.py
release: check
	python3 scripts/release.py
clean:
	rm -rf dist releases
