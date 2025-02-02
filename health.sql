-- Table: Locations
CREATE TABLE Locations (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    description TEXT
);

-- Table: Sensors
CREATE TABLE Sensors (
    sensor_id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_type VARCHAR(100) NOT NULL,
    location_id INT,
    notes TEXT,
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);

-- Table: Sensor_Readings
CREATE TABLE Sensor_Readings (
    reading_id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id INT NOT NULL,
    reading_date DATE NOT NULL,
    reading_time TIME NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pm1 DECIMAL(6,2),
    pm2_5 DECIMAL(6,2),
    pm10 DECIMAL(6,2),
    FOREIGN KEY (sensor_id) REFERENCES Sensors(sensor_id)
);

-- Table: Research_Findings (from KEMRl report)
CREATE TABLE Research_Findings (
    finding_id INT PRIMARY KEY AUTO_INCREMENT,
    report_source VARCHAR(100) NOT NULL,
    section VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    detail TEXT NOT NULL
);

-- Table: Health_Correlations (from Respiratory Correlation Data)
CREATE TABLE Health_Correlations (
    correlation_id INT PRIMARY KEY AUTO_INCREMENT,
    parameter VARCHAR(100) NOT NULL,
    location_id INT,
    detail TEXT NOT NULL,
    value DECIMAL(10,4),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);
