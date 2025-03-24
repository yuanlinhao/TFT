-- Create the Champions table
CREATE TABLE champions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    cost INTEGER NOT NULL,
    health INTEGER NOT NULL,
    attack_damage INTEGER NOT NULL,
    attack_speed FLOAT NOT NULL,
    armor INTEGER NOT NULL,
    magic_resist INTEGER NOT NULL,
    ability_name TEXT NOT NULL,
    ability_description TEXT NOT NULL,
    ability_damage INTEGER NOT NULL,
    mana_cost INTEGER NOT NULL,
    starting_mana INTEGER NOT NULL
);

-- Insert Zoe into Champions table
INSERT INTO champions (name, cost, health, attack_damage, attack_speed, armor, magic_resist, ability_name, ability_description, ability_damage, mana_cost, starting_mana)
VALUES ('Zoe', 4, 800, 40, 0.75, 30, 30, 'Paddle Star!', 'Launches a star at the target, dealing magic damage. It bounces to the farthest enemy within 4 hexes, then bounces back to the target.', 300, 80, 20);

-- Create the Items table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    ability_power INTEGER DEFAULT 0,
    mana INTEGER DEFAULT 0,
    crit_chance FLOAT DEFAULT 0,
    crit_damage FLOAT DEFAULT 0,
    bonus_effect TEXT
);

-- Insert Magic Items into Items table
INSERT INTO items (name, ability_power, crit_chance, crit_damage, bonus_effect)
VALUES ('Jeweled Gauntlet', 10, 20, 10, 'Abilities can critically strike. If the holder''s abilities can already critically strike, gain 10% Critical Strike Damage instead.'),
       ('Rabadon''s Deathcap', 50, 0, 0, 'Deal 15% bonus damage.'),
       ('Archangel''s Staff', 20, 0, 0, 'Combat start: Grant 30 Ability Power every 5 seconds.');

-- Create the Champion-Items relationship table
CREATE TABLE champion_items (
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    PRIMARY KEY (champion_id, item_id)
);
