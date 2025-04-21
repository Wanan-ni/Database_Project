# ChatDB
USC DSCI551 2025 Spring Project


# Instructions

Note: removing "generate mongodb query:", llm can generate sql query.

### Step 1 switch to certain database
```sql
generate mongodb query: use nlq_db database
```
### Step 2 choose a collection
```sql
generate mongodb query: show me all tables of nlq_db
```
### Step 3 construct in your query

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

generate mongodb query: find 5 candidate whose major is computer science(case insensetive), please return their candidate_id, insititution_name and their degree, you should sort by their insititution_name, using method find


#Aggregate
generate mongodb query: Count how many distinct candidates there are for each degree type, return it by sorting degree type
    
generate mongodb query: find candidates(can be many) with the most experience, and return their candidate_id, address, and experience count.

generate mongodb query: find how many distinct candidates meet following constraints: they used to be "Software Engineer" and their degree_name is "PhD"(hint: to get correct answer, we need to use three table)



```