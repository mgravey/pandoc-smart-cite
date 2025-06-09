from setuptools import setup

setup(
	name='pandoc-smart-cite',
	version='0.2',
	description='A Pandoc filter for automatically fetching and caching DOI/arXiv BibTeX entries',
	author='Mathieu Gravey',
	author_email='reserach@mgravey.com',
	url='https://github.com/mgravey/pandoc-smart-cite',
	py_modules=['smart_cite'],
	entry_points={
		'console_scripts': [
			'smart-cite = smart_cite:main',
		],
	},
	install_requires=[
		'panflute',
		'requests',
	],
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
	],
	python_requires='>=3.6',
)
