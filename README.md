# ChatDB

USC DSCI551 2025 Spring Project

# Overview

- Model: Gemini 2.0 Flash
- Databases: MySQL, MongoDB
- Dataset: Subset of [Resume Dataset (Kaggle)](https://www.kaggle.com/datasets/saugataroyarghya/resume-dataset)
- Schema: `candidates`, `education`, `experience` used in both MySQL and MongoDB

# How to Use ChatDB

1. **Start the backend server**

In one terminal, run:

```bash
python main.py
```

Once the server is running at `http://127.0.0.1:5000`, leave this terminal open.


2. **Run the client interface**

In another terminal, run:

```bash
python client.py
```

You will be prompted to input natural language queries:

```bash
please input your query:
```



3. **Exit**

Type `exit` or `quit` to close the client.


# Mysql Instructions

### Switch to certain database

```sql
use nlq_db database
```

### Schema Exploration

```sql
-- Ask what tables exist
generate sql query: show me all tables of nlq_db

-- View schema of tables
generate sql query: describe the schema of candidate table in nlq_db
generate sql query: list all the columns in the candidate table

-- Retrieve sample rows
generate sql query: show 5 example rows from the experience table
```


### CRUD

```sql
#insert
- generate sql query: insert One example to candidate table, information is candidate_id=11111, career_objective="Make more money"
- generate sql query: insert One example to candidate table, information is candidate_id=22222, career_objective="Make more money"
- generate sql query: insert One example to candidate table, information is candidate_id=33333, career_objective="Make more money"

To verify insertion: generate sql query: show me all candidates whose career_objective is "Make more money"

#delete
- generate sql query: delete One example whose candidate_id is 11111
- generate sql query: delete examples whose career_objective is "Make more money"

To verify deletion: generate sql query: show me all candidates whose career_objective is "Make more money"

#update
update one row
- generate sql query: insert one candidate whose candidate_id is 99999 and address is "LA"
- generate sql query: show the address of candidate whose candidate_id is 99999
- generate sql query: update the address of candidate whose candidate_id is 99999 to "New York"
- generate sql query: show the address of candidate whose candidate_id is 99999

update multiple rows
- generate sql query: If candidates passing_year smaller than 2020, sbutract 1 from the value of passing_year
- generate sql query: If candidates passing_year >= 2020, sbutract 1 from the value of passing_year

#Find
- generate sql query: find distinct candidates all information if their career_objective mentioned AI
- generate sql query: find the number of distinct candidates whose career_objective mentioned AI
- generate sql query: find 5 candidate whose major is computer science(case insensetive), please return their candidate_id, insititution_name and their degree, you should sort by their insititution_name
#ORDER BY, LIMIT

#Aggregate
#SUM, ORDER BY
- generate sql query: Count how many distinct candidates there are for each degree type, return it by sorting degree type
# HAVING, GROUP BY,
- generate sql query: find all candidates whose number of experiences equals to the absolute maximum number of experiences. Return their candidate_id and the count of their experiences.

# JOIN
- generate sql query: find how many distinct candidates meet following constraints: they used to be "Software Engineer" and their degree_name is "PhD"(hint: to get correct answer, we need to use three table)
```


# Mongodb Instructions

### Show collections info
```sql
generate mongodb query: show me all collections of nlq_db
 ```
 ```sql
generate mongodb query: show me schema of all collections in nlq_db
```
### CRUD


#### insertOne
```sql
generate mongodb query: insert One example to candidates collection, information is {"candidate_id": 11111, "career_objective":"Make more money"}
```        
#### insertMany
```sql
generate mongodb query: insert Many examples to candidates collection, information is {"candidate_id": 22222, "career_objective":"Make more money"}, {"candidate_id": 44444, "career_objective":"Make more money"}, {"candidate_id": 33333, "career_objective":"Make more money"}
```
#### deleteOne
```sql         
generate mongodb query: delete One example whose candidate_id is 11111
```
#### deleteMany
```sql
generate mongodb query: delete examples whose career_objective is "Make much money"
```
#### updateOne
```sql
generate mongodb query: update one example: derement only one candidate passing_year whose passing_year smaller than 2020
```
#### updateMany
```sql
generate mongodb query: If candidates passing_year smaller than 2020, derement by 1
```
#### Find
```sql
generate mongodb query: Find candidates all information if their career_objective mentioned AI
```

```sql
generate mongodb query: find the number of candidates whose career_objective mentioned AI, using method find and count
```

#### Aggregate 

$project, $sort, $count
```sql
generate mongodb query: Count how many distinct candidates there are for each degree type, return it by sorting degree type
```
$sort, $limit, $group
```sql
generate mongodb query: find 5 candidates whose experience number is bigger or equals than 2,  return their candidate id, and experience count and sorting by their candidate id
```
```sql
generate mongodb query: find 5 candidate whose major is computer science(case insensetive), please return their candidate_id, insititution_name and their degree, you should sort by their insititution_name, using method find
```
lookup, $group, $project
```sql
generate mongodb query: find how many distinct candidates meet following constraints: they used to be "Software Engineer" and their degree_name is "PhD"(hint: to get correct answer, we need to use three table)
```