-- Usamos la base de datos predeterminada de Aiven
USE defaultdb;

-- Creacion de tablas
CREATE TABLE IF NOT EXISTS clientes(
  id INT PRIMARY KEY AUTO_INCREMENT,
  dni INT,
  nombre VARCHAR(50),
  apellido VARCHAR(50),
  telefono VARCHAR(50),
  email VARCHAR(50),
  password VARCHAR(50),
  tipo_usuario INT
);

CREATE TABLE IF NOT EXISTS productos(
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(50),
  precio DOUBLE,
  descripcion TEXT(500),
  img VARCHAR(255),
  categoria ENUM('Perros','Gatos','Otros')
);

CREATE TABLE IF NOT EXISTS consejos(
  id INT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(255),
  texto TEXT(2048)
);

CREATE TABLE IF NOT EXISTS prod_ctes(
  id INT PRIMARY KEY AUTO_INCREMENT,
  idProducto INT,
  idCliente INT,
  FOREIGN KEY (idCliente) REFERENCES clientes(id),
  FOREIGN KEY (idProducto) REFERENCES productos(id)
);

-- Carga de productos
INSERT INTO productos (nombre, precio, descripcion, img, categoria) VALUES
('Alimento Gato', 1200, 'El mejor alimento para tu Gato', 'gato01.png', 'Gatos'),
('Alimento Gato', 4000, 'El mejor alimento para tu Gato', 'gato02.png', 'Gatos'),
('Alimento Gato', 3400, 'El mejor alimento para tu Gato', 'gato03.png', 'Gatos'),
('Alimento Gato', 2300, 'El mejor alimento para tu Gato', 'gato04.png', 'Gatos'),
('Alimento Gato', 5700, 'El mejor alimento para tu Gato', 'gato05.png', 'Gatos'),
('Alimento Gato', 3500, 'El mejor alimento para tu Gato', 'gato06.png', 'Gatos'),
('Piedras sanitarias Gato', 3100, 'Super absorventes', 'perro07.png', 'Gatos'),
('Piedras sanitarias Gato', 2300, 'Super absorventes', 'perro08.png', 'Gatos'),
('Piedras sanitarias Gato', 900, 'Super absorventes', 'perro09.png', 'Gatos'),
('Piedras sanitarias Gato', 2200, 'Super absorventes', 'perro10.png', 'Gatos'),
('Piedras sanitarias Gato', 1700, 'Super absorventes', 'perro11.png', 'Gatos'),
('Piedras sanitarias Gato', 1100, 'Super absorventes', 'perro12.png', 'Gatos'),
('Alimento Perro', 5600, 'El mejor alimento para tu Perro', 'perro01.png', 'Perros'),
('Alimento Perro', 7100, 'El mejor alimento para tu Perro', 'perro02.png', 'Perros'),
('Alimento Perro', 4800, 'El mejor alimento para tu Perro', 'perro03.png', 'Perros'),
('Alimento Perro', 3400, 'El mejor alimento para tu Perro', 'perro04.png', 'Perros'),
('Alimento Perro', 8200, 'El mejor alimento para tu Perro', 'perro05.png', 'Perros'),
('Alimento Perro', 1000, 'El mejor alimento para tu Perro', 'perro06.png', 'Perros'),
('Snack para Perro', 500, 'Snack saludable', 'perro07.png', 'Perros'),
('Snack para Perro', 200, 'Snack saludable', 'perro08.png', 'Perros'),
('Snack para Perro', 1100, 'Snack saludable', 'perro09.png', 'Perros'),
('Snack para Perro', 800, 'Snack saludable', 'perro10.png', 'Perros'),
('Snack para Perro', 2000, 'Snack saludable', 'perro11.png', 'Perros'),
('Snack para Perro', 300, 'Snack saludable', 'perro12.png', 'Perros'),
('Juguete Hamster', 3200, 'La mejor opcion para tu Hamster', 'otros01.png', 'Otros'),
('Juguete Hamster', 4500, 'La mejor opcion para tu Hamster', 'otros02.png', 'Otros'),
('Juguete Hamster', 1100, 'La mejor opcion para tu Hamster', 'otros03.png', 'Otros'),
('Juguete Hamster', 2700, 'La mejor opcion para tu Hamster', 'otros04.png', 'Otros'),
('Juguete Hamster', 6100, 'La mejor opcion para tu Hamster', 'otros05.png', 'Otros'),
('Juguete Hamster', 1500, 'La mejor opcion para tu Hamster', 'otros06.png', 'Otros');

-- Carga de clientes
INSERT INTO clientes (dni, nombre, apellido, telefono, email, password, tipo_usuario) VALUES
(33033033, 'Analía', 'Rossotti', '11111111', 'analia.rossotti@gmail.com', 'Admin123', 1),
(33022022, 'Analía', 'Rossotti', '11111111', 'abraries@hotmail.com', 'Admin123', 1),
(22229999, 'Rosa', 'Solis', '1122229999', 'rosa.solis@gmail.com', 'abc123', 0),
(44554455, 'Pedro', 'Paez', '1144554455','pedro.paez@gmail.com', 'abc123', 0),
(67673434, 'Estela', 'Maldonado', '1167673434', 'estela.maldonado@gmail.com', 'abc123', 0),
(53535353, 'Ambar', 'Kim', '1153535353', 'ambar.kim@gmail.com', 'abc123', 0),
(87878787, 'Balto', 'Gomez','1187878787', 'balto.gomez@gmail.com', 'abc123', 0),
(82342586, 'Dante', 'Cardozo', '1182342586', 'dante.cardozo@gmail.com', 'abc123', 0);

-- Carga de consejos
INSERT INTO consejos (titulo, texto) VALUES
('¿Cómo cuidar a tu mascota?', 'Dejale agua disponible siempre. Asegurate de que esté fresca y limpia. Brindale un lugar cómodo: tu mascota debe tener un lugar para descansar que lo proteja del frío, del calor y de la lluvia. Cuidá su salud: llevala al veterinario una vez al año y tené al día su plan de vacunación y desparasitación.'),
('12 cosas que no debes hacerle nunca a un gato', 'No utilices tus manos o pies para jugar con él. Si quieres conservarlos, usa juguetes para gatos. No le tires contra el juguete, tira el juguete en una trayectoria que se aleja del gato para que él pueda cazarlo. No le eduques a golpes o gritos. Conseguirás que el gato te coja miedo o se defienda. No le persigas, no le grites y no lo mires fijamente si quieres que venga. Dale tiempo y espacio. No le arrincones ni lo bloquees para acariciarlo. No aproveches cuando duerme para molestarle. No le molestes cuando hace sus necesidades. No le tires de la cola. No le rasques la barriga, las patas o la cola. No lo levantes por la piel del cuello. No lo cojas en brazos sin haberte asegurado antes de que le gusta.'),
('Tips para cuidar a tu perro', 'Acaricia a tu perro: un trato amoroso es muy aconsejable para la salud de tu mascota. Hazle hacer ejercicio: emplea unos minutos de tu día para jugar con él. Educa a tu perro: horarios de comidas, salidas, espacios donde dormir. Premia su buen comportamiento. Visitas al veterinario regulares. Buena alimentación e higiene.'),
('¿Cómo me acerco a un perro que no conozco?', 'Pedí permiso a sus dueños. Estirá tu mano y espera que se acerque a olfatearla. Acaricialo suavemente en el lomo. Hablale con voz calma. Nunca acerques tu cara a la del perro. No le acaricies las patas o la cola. No lo mires directamente a los ojos.'),
('Tu gato necesita ciertos cuidados que muchas veces se pasan por alto', 'Protección en las ventanas/balcones con mallas. Bandeja Sanitaria limpia y accesible. Recreación con juegos en altura y rascadores. Un trato respetuoso con afecto y atención. Identificación siempre con collar y chapita.');