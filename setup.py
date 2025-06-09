from setuptools import setup

setup(
	name='pandoc-smart-cite',
	version='0.1',
	description='A Pandoc filter for automatically fetching and caching DOI/arXiv BibTeX entries',
	author='Mathieu Gravey',
	author_email='reserach@mgravey.com',
	url='https://github.com/mgravey/pandoc-smart-cite',
	py_modules=['smart_cite'],
	install_requires=[
		'panflute',
		'requests',
	],
	entry_points={},
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
	],
	python_requires='>=3.6',
)
