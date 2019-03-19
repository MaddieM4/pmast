dist: setup.py $(wildcard pmast/*)
	python setup.py sdist bdist_wheel

upload: dist
	twine upload dist/*

clean:
	rm -rf build dist
