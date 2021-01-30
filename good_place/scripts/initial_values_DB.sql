CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
insert into conditions (id, label) values (uuid_generate_v4(), 'For parts or not working');
insert into conditions (id, label) values (uuid_generate_v4(), 'Acceptable');
insert into conditions (id, label) values (uuid_generate_v4(), 'Good');
insert into conditions (id, label) values (uuid_generate_v4(), 'Very good');
insert into conditions (id, label) values (uuid_generate_v4(), 'New');

insert into categories (id, label, image, icon) values (uuid_generate_v4(), 'Gaming', 'https://cdn.pixabay.com/photo/2017/05/08/02/22/game-2294201_960_720.jpg', 'gamepad');
insert into categories (id, label, image, icon) values (uuid_generate_v4(), 'vehicules', 'https://cdn.pixabay.com/photo/2016/04/07/06/53/bmw-1313343_960_720.jpg', 'truck');
insert into categories (id, label, image, icon) values (uuid_generate_v4(), 'Pets', 'https://cdn.pixabay.com/photo/2017/07/25/01/22/cat-2536662_960_720.jpg', 'paw');
insert into categories (id, label, image, icon) values (uuid_generate_v4(), 'Electronics', 'https://cdn.pixabay.com/photo/2014/09/20/13/52/board-453758_960_720.jpg', 'desktop');
insert into categories (id, label, image, icon) values (uuid_generate_v4(), 'Sports', 'https://cdn.pixabay.com/photo/2013/03/19/18/23/mountain-biking-95032_960_720.jpg', 'volleyball-ball');
insert into categories (id, label, image, icon) values (uuid_generate_v4(), 'Clothes', 'https://cdn.pixabay.com/photo/2015/11/07/11/46/fashion-1031469_960_720.jpg', 'tshirt');
insert into categories (id, label, image, icon) values (uuid_generate_v4(), 'Others', 'https://cdn.pixabay.com/photo/2016/03/27/22/04/camera-1284459_960_720.jpg', 'ellipsis-h');