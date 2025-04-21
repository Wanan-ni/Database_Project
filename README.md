# ChatDB
USC DSCI551 2025 Spring Project

# Mysql Instructions
### Switch to certain database
```sql
use nlq_db database
```
### Show collections info
```sql
generate sql query: show me all tables of nlq_db
generate sql query: show me schema of all tables in nlq_db
generate sql query: lists all the columns in the candidate
```
### CRUD

```sql
#insert
1) generate sql query: insert One example to candidate table, information is candidate_id=11111, career_objective="Make more money"
2) generate sql query: insert One example to candidate table, information is candidate_id=22222, career_objective="Make more money"
3) generate sql query: insert One example to candidate table, information is candidate_id=33333, career_objective="Make more money"
         
#delete
4) generate sql query: delete One example whose candidate_id is 11111
5) generate sql query: delete examples whose career_objective is "Make more money"

#update
6) generate sql query: If candidates passing_year smaller than 2020, sbutract 1 from the value of passing_year
7) generate sql query: If candidates passing_year >= 2020, sbutract 1 from the value of passing_year

#Find
8) generate sql query: find distinct candidates all information if their career_objective mentioned AI
9) generate sql query: find the number of distinct candidates whose career_objective mentioned AI
10) generate sql query: find 5 candidate whose major is computer science(case insensetive), please return their candidate_id, insititution_name and their degree, you should sort by their insititution_name
#ORDER BY, LIMIT

#Aggregate
#SUM, ORDER BY
generate sql query: Count how many distinct candidates there are for each degree type, return it by sorting degree type
# HAVING, GROUP BY, 
generate sql query: find all candidates whose number of experiences equals to the absolute maximum number of experiences. Return their candidate_id and the count of their experiences.
# JOIN
generate sql query: find how many distinct candidates meet following constraints: they used to be "Software Engineer" and their degree_name is "PhD"(hint: to get correct answer, we need to use three table)
```



# Mongodb Instructions

### Switch to certain database
```sql
generate mongodb query: use nlq_db database
```
### Show collections info
```sql
generate mongodb query: show me all collections of nlq_db
generate mongodb query: show me schema of all collections in nlq_db
```
### CRUD

```sql
#insertOne
generate mongodb query: insert One example to candidates collection, information is {"candidate_id": 11111, "career_objective":"Make more money"}

#insertMany
generate mongodb query: insert Many examples to candidates collection, information is {"candidate_id": 22222, "career_objective":"Make more money"}, {"candidate_id": 44444, "career_objective":"Make more money"}, {"candidate_id": 33333, "career_objective":"Make more money"}

#deleteOne
generate mongodb query: delete One example whose candidate_id is 11111

#deleteMany
generate mongodb query: delete examples whose career_objective is "Make much money"

#updateOne
generate mongodb query: update one example: derement only one candidate passing_year whose passing_year smaller than 2020

#updateMany
generate mongodb query: If candidates passing_year smaller than 2020, derement by 1

#Find
generate mongodb query: Find candidates all information if their career_objective mentioned AI
generate mongodb query: find the number of candidates whose career_objective mentioned AI, using method find and count


#Aggregate 

#$project, $sort, $count
generate mongodb query: Count how many distinct candidates there are for each degree type, return it by sorting degree type

#$sort, $limit, $group
generate mongodb query: find 5 candidates whose experience number is bigger or equals than 2,  return their candidate id, and experience count and sorting by their candidate id
generate mongodb query: find 5 candidate whose major is computer science(case insensetive), please return their candidate_id, insititution_name and their degree, you should sort by their insititution_name, using method find

#$lookup, $group, $project
generate mongodb query: find how many distinct candidates meet following constraints: they used to be "Software Engineer" and their degree_name is "PhD"(hint: to get correct answer, we need to use three table)
```