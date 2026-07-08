-- Reference DDL for the Azure SQL Database schema.
-- The app also creates these tables automatically on startup
-- (SQLAlchemy Base.metadata.create_all), so running this manually
-- is optional but useful for review or manual provisioning.

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE Users (
        user_id        INT IDENTITY(1,1) PRIMARY KEY,
        username       NVARCHAR(100) NOT NULL UNIQUE,
        password_hash  NVARCHAR(255) NOT NULL,
        created_at     DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'UserData')
BEGIN
    CREATE TABLE UserData (
        record_id    INT IDENTITY(1,1) PRIMARY KEY,
        user_id      INT NOT NULL FOREIGN KEY REFERENCES Users(user_id),
        topic        NVARCHAR(100) NOT NULL,
        description  NVARCHAR(255) NULL,
        updated_at   DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );

    CREATE INDEX IX_UserData_user_id_topic ON UserData(user_id, topic);
END;
