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
