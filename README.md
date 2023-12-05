astrotemplate-db
---------------------------
A template for astronomical databases.

We encourage users to follow the detailed best practices for astronomical databases outlined in [Chen et al. 2022](https://iopscience.iop.org/article/10.3847/1538-4365/ac6268).

installation instructions
---------------------------
All you should need to run is:

`pip install .`

If you'd liek to ensure that the package has been installed correctly, you can run

`pip install .[test]`

then run

`pytest tests`

These commands will download the `pytest` package and run this codebase's test suite, respectively.
