CREATE DATABASE globanttest;

USE globanttest;
	CREATE TABLE departments (
	id smallint primary key,
	department varchar(200)
	);

	CREATE TABLE jobs (
	id smallint primary key,
	names varchar(200)
	);

	CREATE TABLE hired_employees (
	id smallint primary key,
	names varchar(200),
	datetimeshired datetime,
	departament_id smallint,
	job_id smallint,
	FOREIGN KEY (departament_id) REFERENCES departments (id),
	FOREIGN KEY (job_id) REFERENCES jobs (id)
	);