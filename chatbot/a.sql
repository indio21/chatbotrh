-- Inserción de empleados
INSERT INTO empleados (id, nombre, email, puesto) VALUES 
(1, 'Juan Pérez', 'juan@empresa.com', 'Analista'),
(2, 'Lucía Gómez', 'lucia@empresa.com', 'Desarrolladora'),
(3, 'Carlos López', 'carlos@empresa.com', 'Jefe de RRHH'),
(4, 'Ana Martínez', 'ana@empresa.com', 'Administrativa'),
(5, 'Pedro Díaz', 'pedro@empresa.com', 'Gerente');

-- Inserción de vacaciones
INSERT INTO vacaciones (empleado_id, dias_total, dias_utilizados) VALUES
(1, 15, 7),
(2, 20, 10),
(3, 25, 5),
(4, 18, 18),
(5, 30, 12);
