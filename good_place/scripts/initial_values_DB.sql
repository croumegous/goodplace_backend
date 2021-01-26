CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
insert into conditions (id, label) values (uuid_generate_v4(), 'For parts or not working');
insert into conditions (id, label) values (uuid_generate_v4(), 'Acceptable');
insert into conditions (id, label) values (uuid_generate_v4(), 'Good');
insert into conditions (id, label) values (uuid_generate_v4(), 'Very good');
insert into conditions (id, label) values (uuid_generate_v4(), 'New');

insert into categories (id, label) values (uuid_generate_v4(), 'Gaming');
insert into categories (id, label) values (uuid_generate_v4(), 'Sports');
insert into categories (id, label) values (uuid_generate_v4(), 'vehicules');
insert into categories (id, label) values (uuid_generate_v4(), 'Pets');
insert into categories (id, label) values (uuid_generate_v4(), 'Electronics');
insert into categories (id, label) values (uuid_generate_v4(), 'Sports');
insert into categories (id, label) values (uuid_generate_v4(), 'Clothes');
insert into categories (id, label) values (uuid_generate_v4(), 'Others');