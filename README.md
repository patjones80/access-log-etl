# access-log-etl

Pull website access log in .txt format to a Postgres database.

## About

This code was developed to extract website access logs in raw .txt format into a Postgres SQL database. Having the log data in SQL opens up many possibilities for analysis, and provides an alternative to Google Analytics for developers who are well-versed in text parsing and writing SQL, but may not want to navigate the maze of functionality in Google Analytics to answer basic questions. 

I provide the Python script used for the extraction as well as SQL queries that have been helpful in working with the resulting dataset.

## Built With

Python3 and SQL; AWS EC2 and RDS environment

## Creator/Maintainer

Patrick Jones - [patjones80@gmail.com](mailto:patjones80@gmail.com)
