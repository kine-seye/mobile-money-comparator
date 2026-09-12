-- insertion des opérateur eu sénégal
insert into operateurs(nom) values
('Wave'),
('Orange money'),
('Free money')
ON CONFLICT (nom) DO NOTHING;

-- insertion des types d'opérateur de base
insert into types_operation(nom) values
('Retrait'),
('Depot'),
('Transfert'),
('Paiment Marchand')
ON CONFLICT (nom) DO NOTHING;