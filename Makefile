.SILENT:

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -rf {} \;

	rm -rf build

test: clean
	python manage.py test --settings=settings_test
