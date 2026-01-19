USE INE;

-- UNSIGNED: No permite valores negativos
-- DECIMAL(18,4): 18 digitos en total (ultimos 4 son decimales)

-- Creo la tabla de descripcion IPC_DESC
CREATE TABLE t_ipc_desc (
    id_division TINYINT UNSIGNED NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_division)
) ENGINE=InnoDB;

-- Creo la tabla de descripcion IMS
CREATE TABLE t_ipc (
    periodo DATE NOT NULL,
    id_division TINYINT UNSIGNED NOT NULL,
    ponderacion DECIMAL(18,4) NOT NULL,
    indice DECIMAL(18,4) NOT NULL,
    var_mensual DECIMAL(18,4) NOT NULL,
    var_ac_anual DECIMAL(18,4) NOT NULL,
    var_doce_meses DECIMAL(18,4) NOT NULL,
    incidencia DECIMAL(18,4) NOT NULL,
    PRIMARY KEY (periodo, id_division),
    CONSTRAINT fk_ipc_division
        FOREIGN KEY (id_division)
        REFERENCES t_ipc_desc (id_division)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;


-- Creo la tabla de descripcion IMS
CREATE TABLE t_ims_desc (
    id_sector CHAR(1) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_sector)
) ENGINE=InnoDB;

-- Creo la tabla donde se almaceran los datos de IMS
CREATE TABLE t_ims (
	periodo DATE NOT NULL,
	id_sector CHAR(1) NOT NULL,
	indice DECIMAL(18,4) NOT NULL,
	mes DECIMAL(18,4) NOT NULL,
	acum_anual DECIMAL(18,4) NOT NULL,
    ultimos_doce_meses DECIMAL(18,4) NOT NULL,
    incidencias DECIMAL(18,4) NOT NULL,
    PRIMARY KEY (periodo, id_sector),
    CONSTRAINT fk_ims_sector
        FOREIGN KEY (id_sector)
        REFERENCES t_ims_desc (id_sector)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;


-- Creo la tabla de descripcion ICCV
CREATE TABLE t_iccv_desc (
    id_rubro TINYINT UNSIGNED NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_rubro)
) ENGINE=InnoDB;

-- Creo la tabla donde se almacenaran los datos de IMS
CREATE TABLE t_iccv (
    periodo DATE NOT NULL,
    id_rubro TINYINT UNSIGNED NOT NULL,
    indice DECIMAL(18,4) NOT NULL,
    var_mensual DECIMAL(18,4) NOT NULL,
    incidencias DECIMAL(18,4) NOT NULL,
    PRIMARY KEY (periodo, id_rubro),
    CONSTRAINT fk_iccv_rubro
        FOREIGN KEY (id_rubro)
        REFERENCES t_iccv_desc (id_rubro)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;


-- Muestra las tablas creadas
SHOW TABLES;

-- Elimina una tabla
DROP TABLES t_ipc;

-- Elimina todos los registros de una tabla
TRUNCATE TABLE t_ipc;
TRUNCATE TABLE t_ims;
TRUNCATE TABLE t_iccv;
