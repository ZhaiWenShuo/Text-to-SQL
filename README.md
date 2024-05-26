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
> "Continent" INTEGER,
> FOREIGN KEY (Continent) REFERENCES continents(ContId));
> \# CREATE TABLE "car\_makers" (
> "Id" INTEGER PRIMARY KEY,
> "Maker" TEXT,
> "FullName" TEXT,
> "Country" TEXT,
> FOREIGN KEY (Country) REFERENCES countries(CountryId));
> \# CREATE TABLE "model\_list" (
> "ModelId" INTEGER PRIMARY KEY,
> "Maker" INTEGER,
> "Model" TEXT UNIQUE,
> FOREIGN KEY (Maker) REFERENCES car\_makers (Id));
> \# CREATE TABLE "car\_names" (
> "MakeId" INTEGER PRIMARY KEY,
> "Model" TEXT,
> "Make" TEXT,
> FOREIGN KEY (Model) REFERENCES model\_list (Model));
> \# CREATE TABLE "cars\_data" (
> "Id" INTEGER PRIMARY KEY,
> "MPG" TEXT,
> "Cylinders" INTEGER,
> "Edispl" REAL,
> "Horsepower" TEXT,
> "Weight" INTEGER,
> "Accelerate" REAL, 
> "Year" INTEGER,
> FOREIGN KEY (Id) REFERENCES car\_names (MakeId));
