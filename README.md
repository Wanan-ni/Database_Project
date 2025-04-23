# ChatDB
USC DSCI551 2025 Spring Project

# Mysql Instructions

### Show collections info
```sql
generate sql query: show me all tables of nlq_db
```

```sql
generate sql query: lists all the columns in the candidate
```
### CRUD


#### insert

```sql
generate sql query: insert One example to candidate table, information is candidate_id=11111, career_objective="Make more money"
```
```sql
generate sql query: insert One example to candidate table, information is candidate_id=22222, career_objective="Make more money"
```
```sql
generate sql query: insert One example to candidate table, information is candidate_id=33333, career_objective="Make more money"
```
#### delete
```sql
generate sql query: delete One example whose candidate_id is 11111
```
```sql
generate sql query: delete examples whose career_objective is "Make more money"
```
#### update
```sql
generate sql query: If candidates passing_year smaller than 2020, sbutract 1 from the value of passing_year
```
```sql
generate sql query: If candidates passing_year >= 2020, sbutract 1 from the value of passing_year
```
#### find
```sql
generate sql query: find distinct candidates all information if their career_objective mentioned AI
```
COUNT, DISTINCT
```sql
generate sql query: find the number of distinct candidates whose career_objective mentioned AI
```
ORDER BY, LIMIT
```sql
generate sql query: find 5 candidate whose major is computer science(case insensetive), please return their candidate_id, insititution_name and their degree, you should sort by their insititution_name
```

#### Aggregate
SUM, ORDER BY
```sql
generate sql query: Count how many distinct candidates there are for each degree type, return it by sorting degree type
```
HAVING, GROUP BY
```sql
generate sql query: find all candidates whose number of experiences equals to the absolute maximum number of experiences. Return their candidate_id and the count of their experiences.
```
JOIN, DISTINCT
```sql
generate sql query: find how many distinct candidates meet following constraints: they used to be "Software Engineer" and their degree_name is "PhD"(hint: to get correct answer, we need to use three table)
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