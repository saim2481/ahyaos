-- Stored Procedure 1: Select vehicles with null PoliceStation (Truly Optional CityCode)
CREATE OR ALTER PROCEDURE SelectVehiclesWithNullPoliceStation
    @PSName NVARCHAR(100),
    @CityCode INT = NULL
AS
BEGIN
    DECLARE @SQL NVARCHAR(MAX);
    
    SET @SQL = N'
    SELECT * FROM Vehicle_PoliceCrime 
    WHERE VehicleId IN (
        SELECT VehicleId 
        FROM Vehicle_Registration 
        WHERE OldComplaintNumber IN ( 
            SELECT cp.compno 
            FROM testCPLC_p3.dbo.complainpolice cp 
            INNER JOIN testCPLC_p3.dbo.policeinfo ci 
                ON cp.pscode = ci.pscode 
                AND cp.twncode = ci.twncode 
                AND cp.discode = ci.discode 
                AND ci.divcode = cp.divcode 
            WHERE ci.psname = @PSName'
    
    IF @CityCode IS NOT NULL
        SET @SQL = @SQL + N' AND cp.ctycode = @CityCode'
    
    SET @SQL = @SQL + N'
        )
    ) 
    AND PoliceStation IS NULL;'
    
    EXEC sp_executesql @SQL, N'@PSName NVARCHAR(100), @CityCode INT', @PSName, @CityCode;
END
GO

-- Stored Procedure 2: Update vehicles with null PoliceStation (Truly Optional CityCode)
CREATE OR ALTER PROCEDURE UpdateVehiclesWithNullPoliceStation
    @PSName NVARCHAR(100),
    @NewPoliceStation INT,
    @CityCode INT = NULL
AS
BEGIN
    DECLARE @SQL NVARCHAR(MAX);
    
    SET @SQL = N'
    UPDATE Vehicle_PoliceCrime 
    SET PoliceStation = @NewPoliceStation
    WHERE VehicleId IN (
        SELECT VehicleId 
        FROM Vehicle_Registration 
        WHERE OldComplaintNumber IN ( 
            SELECT cp.compno 
            FROM testCPLC_p3.dbo.complainpolice cp 
            INNER JOIN testCPLC_p3.dbo.policeinfo ci 
                ON cp.pscode = ci.pscode 
                AND cp.twncode = ci.twncode 
                AND cp.discode = ci.discode 
                AND ci.divcode = cp.divcode 
            WHERE ci.psname = @PSName'
    
    IF @CityCode IS NOT NULL
        SET @SQL = @SQL + N' AND cp.ctycode = @CityCode'
    
    SET @SQL = @SQL + N'
        )
    ) 
    AND PoliceStation IS NULL;'
    
    EXEC sp_executesql @SQL, N'@PSName NVARCHAR(100), @NewPoliceStation INT, @CityCode INT', @PSName, @NewPoliceStation, @CityCode;
END
GO


EXEC SelectVehiclesWithNullPoliceStation 
    @PSName = 'CITY KHANEWAL'
    @CityCode = 61;