USE INE;

-- Elimino la StoredProcedure en caso que ya exista
DROP PROCEDURE IF EXISTS sp_total_rows;

-- Creo la nueva StoredProcedure
CREATE PROCEDURE sp_total_rows (
    IN tablename VARCHAR(64),
    OUT nrows BIGINT
)
BEGIN
    -- 1. Preparo sentencia concatenando el nombre de la tabla
    SET @sql_stmt = CONCAT('SELECT COUNT(*) INTO @row_count FROM ', tablename);

    -- 2. Ejecuto sentencia dinámica
    PREPARE stmt FROM @sql_stmt;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- 3. Asigno resultado de la variable al parámetro de salida
    SET nrows = @row_count;
END;

-- Chequeo que haya quedado correctamente creada
SHOW CREATE PROCEDURE sp_total_rows;
