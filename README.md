# Learn From Mistakes: Guidance on Zero-shot Conversational Text-to-SQL

Here we will show the relevant prompts of our paper.

## Database Schema Prompt

> \#\#\# Given the following database schema, your job is to write queries given a user’s request and with no explanation. <br/>
> \# CREATE TABLE "continents" ( <br/>
> "ContId" INTEGER PRIMARY KEY, <br/>
> "Continent" TEXT); <br/>
> \# CREATE TABLE "countries" ( <br/> 
> "CountryId" INTEGER PRIMARY KEY, <br/>
> "CountryName" TEXT, <br/>
> "Continent" INTEGER, <br/>
> FOREIGN KEY (Continent) REFERENCES continents(ContId)); <br/>
> \# CREATE TABLE "car\_makers" ( <br/>
> "Id" INTEGER PRIMARY KEY, <br/>
> "Maker" TEXT, <br/>
> "FullName" TEXT, <br/>
> "Country" TEXT, <br/>
> FOREIGN KEY (Country) REFERENCES countries(CountryId)); <br/>
> \# CREATE TABLE "model\_list" ( <br/>
> "ModelId" INTEGER PRIMARY KEY, <br/>
> "Maker" INTEGER, <br/>
> "Model" TEXT UNIQUE, <br/>
> FOREIGN KEY (Maker) REFERENCES car\_makers (Id)); <br/>
> \# CREATE TABLE "car\_names" ( <br/>
> "MakeId" INTEGER PRIMARY KEY, <br/>
> "Model" TEXT, <br/>
> "Make" TEXT, <br/>
> FOREIGN KEY (Model) REFERENCES model\_list (Model)); <br/>
> \# CREATE TABLE "cars\_data" ( <br/>
> "Id" INTEGER PRIMARY KEY, <br/>
> "MPG" TEXT, <br/>
> "Cylinders" INTEGER, <br/>
> "Edispl" REAL, <br/>
> "Horsepower" TEXT, <br/>
> "Weight" INTEGER, <br/>
> "Accelerate" REAL, <br/>
> "Year" INTEGER, <br/>
> FOREIGN KEY (Id) REFERENCES car\_names (MakeId)); <br/>

## Column Semantic Inference Prompt

The sample tabular data representation format is in json format as an example.

Input:

> \#\#\# Given the following database schema and the first three rows of data from each table as reference, your job is to infer the semantics of table and column to ensure correct table joins based on relationships defined in the database schema. <br/>
> \# CREATE TABLE "continents" ( <br/>
> "ContId" INTEGER PRIMARY KEY, <br/>
> "Continent" TEXT); <br/>
> \# CREATE TABLE "countries" (  <br/>
> "CountryId" INTEGER PRIMARY KEY, <br/>
> "CountryName" TEXT, <br/>
> "Continent" INTEGER, <br/>
> FOREIGN KEY (Continent) REFERENCES continents(ContId)); <br/>
> \# CREATE TABLE "car\_makers" ( <br/>
> "Id" INTEGER PRIMARY KEY, <br/>
> "Maker" TEXT, <br/>
> "FullName" TEXT, <br/>
> "Country" TEXT, <br/>
> FOREIGN KEY (Country) REFERENCES countries(CountryId)); <br/>
> \# CREATE TABLE "model\_list" ( <br/>
> "ModelId" INTEGER PRIMARY KEY, <br/>
> "Maker" INTEGER, <br/>
> "Model" TEXT UNIQUE, <br/>
> FOREIGN KEY (Maker) REFERENCES car\_makers (Id)); <br/>
> \# CREATE TABLE "car\_names" ( <br/>
> "MakeId" INTEGER PRIMARY KEY, <br/>
> "Model" TEXT, <br/>
> "Make" TEXT, <br/>
> FOREIGN KEY (Model) REFERENCES model\_list (Model)); <br/>
> \# CREATE TABLE "cars\_data" ( <br/>
> "Id" INTEGER PRIMARY KEY, <br/>
> "MPG" TEXT, <br/>
> "Cylinders" INTEGER, <br/>
> "Edispl" REAL, <br/>
> "Horsepower" TEXT, <br/>
> "Weight" INTEGER, <br/>
> "Accelerate" REAL,  <br/>
> "Year" INTEGER, <br/>
> FOREIGN KEY (Id) REFERENCES car\_names (MakeId)); <br/>
> \#\# We selected the first three rows of data from each <br/>
> table as reference, as follows:  <br/>
> \# TABLE "continents":  <br/>
> {"ContId":{"0":1,"1":2,"2":3}, <br/>
>  "Continent":{"0":"america","1":"europe","2":"asia"}} <br/>
> \# TABLE "countries":  <br/>
> {"CountryId":{"0":1,"1":2,"2":3}, <br/>
>  "CountryName":{"0":"usa","1":"germany","2":"france"}, <br/>
>  "Continent":{"0":1,"1":2,"2":2}} <br/>
> \# TABLE "car_makers":  <br/>
> {"Id":{"0":1,"1":2,"2":3}, <br/>
>  "Maker":{"0":"amc","1":"volkswagen","2":"bmw"}, <br/>
>  "FullName":{"0":"American Motor Company", <br/>
> 	        "1":"Volkswagen","2":"BMW"}, <br/>
>  "Country":{"0":"1","1":"2","2":"2"}} <br/>
> \# TABLE "model_list":  <br/>
> {"ModelId":{"0":1,"1":2,"2":3}, <br/>
>  "Maker":{"0":1,"1":2,"2":3}, <br/>
>  "Model":{"0":"amc","1":"audi","2":"bmw"}} <br/>
> \# TABLE "car_names":  <br/>
> {"MakeId":{"0":1,"1":2,"2":3}, <br/>
>  "Model":{"0":"chevrolet","1":"buick","2":"plymouth"}, <br/>
>  "Make":{"0":"chevrolet chevelle malibu", <br/>
>  	     "1":"buick skylark 320","2":"plymouth satellite"}} <br/>
> \# TABLE "cars_data":  <br/>
> {"Id":{"0":1,"1":2,"2":3}, <br/>
>  "MPG":{"0":"18","1":"15","2":"18"}, <br/>
>  "Cylinders":{"0":8,"1":8,"2":8}, <br/>
>  "Edispl":{"0":307.0,"1":350.0,"2":318.0}, <br/>
>  "Horsepower":{"0":"130","1":"165","2":"150"}, <br/>
>  "Weight":{"0":3504,"1":3693,"2":3436}, <br/>
>  "Accelerate":{"0":12.0,"1":11.5,"2":11.0}, <br/>
>  "Year":{"0":1970,"1":1970,"2":1970}} <br/>
