--table 1 : les opérateurs
create table operateur(
	id serial primary key,
	nom varchar(50) not null unique
); 
-- les types d'opération
create table type_operation(
	id serial primary key,
	nom varchar(50) not null unique
);

-- les tranches de frias
create table grille_tarifaire(
	id serial primary key,
	operateur_id int references operateur(id),
	type_operation_id int references type_operation(id),
	montant_min numeric(10,2) not null,
	montant_max numeric(10,2),
	frais_fixe numeric(10,2) default 0,
	frais_pourcentage numeric (5,4) default 0,
	dat_maj date not null default current_date,
	source VARCHAR(255)
);


CREATE INDEX idx_grille_lookup
    ON grille_tarifaire (type_operation_id, montant_min, montant_max);
	
	