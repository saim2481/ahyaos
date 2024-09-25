-- Create the IndustrySector table if it doesn't exist
CREATE TABLE IF NOT EXISTS "IndustrySector" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Insert data into the IndustrySector table
INSERT INTO "IndustrySector" (name) VALUES
    ('Agriculture'),
    ('Hunting'),
    ('Forestry'),
    ('Fishing'),
    ('Buildings and infrastructure'),
    ('Consumer Goods and services'),
    ('Education'),
    ('Energy'),
    ('Equipment'),
    ('Health and Social Care'),
    ('Information and communication'),
    ('Insurance and Financial Services'),
    ('Land Use'),
    ('Materials and Manufacturing'),
    ('Organizational Activities'),
    ('Refrigerants and fugitive Gases'),
    ('Restaurants and Accommodation'),
    ('Transport'),
    ('Waste'),
    ('Water');

-- Create the Industry table if it doesn't exist
CREATE TABLE IF NOT EXISTS "Industry" (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    sector_id INT NOT NULL,
    FOREIGN KEY (sector_id) REFERENCES "IndustrySector"(id)
);

-- Example insert into Industry table
-- INSERT INTO "Industry" (company_name, sector_id) VALUES ('Company ABC', 1);
