USE INE;

-- Inserción de datos fijos en t_desc_ipc
INSERT INTO t_ipc_desc (id_division, descripcion) VALUES
(1, 'Alimentos y bebidas no alcoholicas'),
(2, 'Bebidas alcoholicas, tabaco y estupefacientes'),
(3, 'Ropa y calzado'),
(4, 'Vivienda, agua, electricidad, gas y otros combustibles'),
(5, 'Mobiliario, equipo domestico y rutina del hogar'),
(6, 'Salud'),
(7, 'Transporte'),
(8, 'Informacion y comunicacion'),
(9, 'Recreacion, deporte y cultura'),
(10, 'Servicios de educacion'),
(11, 'Restaurantes y alojamientos'),
(12, 'Seguros y servicios financieros'),
(13, 'Cuidado personal, asistencia social y bienes varios');


-- Inserción de datos fijos en t_desc_ims
INSERT INTO t_ims_desc (id_sector, descripcion) VALUES
('D', 'Industrias Manufactureras'),
('F', 'Construccion'),
('G', 'Comercio Al Por Mayor Y Al Por Menor; Reparacion De Vehiculos, Efectos Personales Y Enseres Domesticos'),
('H', 'Hoteles Y Restoranes'),
('I', 'Transporte Almacenamiento Y Comunicaciones'),
('J', 'Intermediacion Financiera'),
('K', 'Actividades Inmobiliarias Empresariales Y De Alquiler'),
('M', 'Enseñanza'),
('N', 'Servicios Sociales Y De Salud');

INSERT INTO t_iccv_desc (id_rubro, descripcion) VALUES
(1, 'Replanteo, implantación y movimiento de tierra'),
(2, 'Hormigón armado'),
(3, 'Albañilería'),
(4, 'Construcciones livianas'),
(5, 'Carpintería'),
(6, 'Herrería'),
(7, 'Aluminio'),
(8, 'Cortinas de enrollar'),
(9, 'Instalación eléctrica'),
(10, 'Instalación sanitaria'),
(11, 'Aparatos y grifería'),
(12, 'Ascensor'),
(13, 'Vidrios'),
(14, 'Pintura'),
(15, 'Equipamiento interior'),
(16, 'Infraestructura'),
(17, 'Gastos generales'),
(18, 'Impuestos'),
(19, 'Leyes sociales'),
(20, 'Permisos de construcción');
