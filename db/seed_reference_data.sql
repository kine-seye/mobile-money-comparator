-- insertion des opérateur eu sénégal
insert into operateurs(nom) values
('Wave'),
('Orange Money'),
('Yas (Mixx by Yas')
ON CONFLICT (nom) DO NOTHING;

-- insertion des types d'opérateur de base
insert into types_operation(nom) values
('retrait'),
('depot'),
('transfert'),
('paiement_marchand')
ON CONFLICT (nom) DO NOTHING;