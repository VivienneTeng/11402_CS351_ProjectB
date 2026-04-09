# 11402_CS351_ProjectB
Project B - CSV Mini Database &amp; Query Engine

## Overview

Project B is a simple CSV mini database and query engine. It demonstrates:
- CSV parsing
- lightweight indexing
- simple query grammar
- performance trade-offs

## Features

- Load CSV files with quoted and escaped fields
- Build an in-memory table representation
- Support basic queries over rows and columns
- Optional use of a third-party CSV parser via package manager

## CSV Parsing

Two common approaches:

1. Write a simple, robust parser
    - handles commas inside quoted fields
    - supports escaped quotes inside quoted values
    - keeps line-oriented parsing for records
    - good for learning and small projects

2. Use a lightweight library via vcpkg or Conan
    - example libraries: fast-cpp-csv-parser, csv-parser
    - reduces parsing edge-case work
    - easier maintenance for production use

## Indexing

- Build indexes on columns to speed up queries
- Common index types:
  - hash-based index for equality lookups
  - sorted index for range and order queries
- Trade-off:
  - faster query performance
  - additional memory and build time

## Query Grammar

A simple query grammar can include:
- SELECT column1, column2
- FROM table
- WHERE column = value
- optional ORDER BY or LIMIT

Example:
- `SELECT name, age FROM data WHERE city = "Seattle"`

Keep grammar small and easy to parse:
- tokenization
- keywords
- column and literal parsing
- boolean expressions for filters

## Performance Trade-offs

- Parsing speed vs correctness
  - handcrafted parser is slower but educational
  - library parser is faster and more reliable
- Memory usage vs query speed
  - indexes use extra memory
  - without indexes, scans are simpler but slower
- Preprocessing time vs runtime query latency
  - build structures once, answer many queries faster

## Build and Usage

- Implement parser and query engine in C++
- Optionally configure dependency manager:
  - `vcpkg install csv-parser`
  - `conan install .`

Document usage examples and command-line options in code or a separate section if needed.