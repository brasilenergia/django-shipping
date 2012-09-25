.SILENT:

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -rf {} \;

	rm -rf build

start: clean
	python manage.py runserver 127.0.0.1:8001

test: clean
	python manage.py test --settings=settings_test
