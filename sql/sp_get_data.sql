USE INE;

-- DATA IPC
DROP PROCEDURE IF EXISTS sp_get_ipc;
CREATE PROCEDURE sp_get_ipc()
BEGIN
    SELECT
        ipc.periodo,
        ipc.id_division,
        dipc.descripcion,
        ipc.ponderacion,
        ipc.indice,
        ipc.var_mensual,
        ipc.var_ac_anual,
        ipc.var_doce_meses,
        ipc.incidencia
    FROM
        t_ipc ipc INNER JOIN t_ipc_desc dipc ON ipc.id_division = dipc.id_division
	ORDER BY
		ipc.periodo,
		ipc.id_division;
END;


-- DATA IMS
DROP PROCEDURE IF EXISTS sp_get_ims;
CREATE PROCEDURE sp_get_ims()
BEGIN
	SELECT
		ims.periodo,
		ims.id_sector,
		dims.descripcion,
		ims.indice,
		ims.mes,
		ims.acum_anual,
		ims.ultimos_doce_meses,
		ims.incidencias
	FROM
		t_ims ims inner join t_ims_desc dims on ims.id_sector = dims.id_sector
	ORDER BY
		ims.periodo,
		ims.id_sector;
END;


-- DATA ICCV
DROP PROCEDURE IF EXISTS sp_get_iccv;
CREATE PROCEDURE sp_get_iccv()
BEGIN
	SELECT
		iccv.periodo,
		iccv.id_rubro,
		diccv.descripcion,
		iccv.indice,
		iccv.var_mensual,
		iccv.incidencias
	FROM
		t_iccv iccv inner join t_iccv_desc diccv on iccv.id_rubro = diccv.id_rubro
	ORDER BY
		iccv.periodo,
		iccv.id_rubro;
END;


-- MOSTRAR TODOS LOS STORED PROCEDURES EXISTENTES
SHOW PROCEDURE STATUS;
