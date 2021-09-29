Database_Name "python_todo";

CREATE TABLE "todo" (
"id" SERIAL PRIMARY KEY,
"task" VARCHAR(250) NOT NULL,
"completed" BOOLEAN DEFAULT FALSE,
"date_added" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"date_completed" VARCHAR DEFAULT NULL
);
