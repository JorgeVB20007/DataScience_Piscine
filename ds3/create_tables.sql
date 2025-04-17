CREATE TABLE IF NOT EXISTS test_knight (
	"Sensitivity" FLOAT,
	"Hability" FLOAT,
	"Strength" FLOAT,
	"Power" FLOAT,
	"Agility" FLOAT,
	"Dexterity" FLOAT,
	"Awareness" FLOAT,
	"Prescience" FLOAT,
	"Reactivity" FLOAT,
	"Midi-chlorien" FLOAT,
	"Slash" FLOAT,
	"Push" FLOAT,
	"Pull" FLOAT,
	"Lightsaber" FLOAT,
	"Survival" FLOAT,
	"Repulse" FLOAT,
	"Friendship" FLOAT,
	"Blocking" FLOAT,
	"Deflection" FLOAT,
	"Mass" FLOAT,
	"Recovery" FLOAT,
	"Evade" FLOAT,
	"Stims" FLOAT,
	"Sprint" FLOAT,
	"Combo" FLOAT,
	"Delay" FLOAT,
	"Attunement" FLOAT,
	"Empowered" FLOAT,
	"Burst" FLOAT,
	"Grasping" FLOAT
);

TRUNCATE test_knight;
COPY test_knight("Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity", "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push", "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking", "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo", "Delay", "Attunement", "Empowered", "Burst", "Grasping")
FROM '/test_knight.csv' DELIMITER ',' CSV HEADER;



CREATE TABLE IF NOT EXISTS train_knight (
	"Sensitivity" FLOAT,
	"Hability" FLOAT,
	"Strength" FLOAT,
	"Power" FLOAT,
	"Agility" FLOAT,
	"Dexterity" FLOAT,
	"Awareness" FLOAT,
	"Prescience" FLOAT,
	"Reactivity" FLOAT,
	"Midi-chlorien" FLOAT,
	"Slash" FLOAT,
	"Push" FLOAT,
	"Pull" FLOAT,
	"Lightsaber" FLOAT,
	"Survival" FLOAT,
	"Repulse" FLOAT,
	"Friendship" FLOAT,
	"Blocking" FLOAT,
	"Deflection" FLOAT,
	"Mass" FLOAT,
	"Recovery" FLOAT,
	"Evade" FLOAT,
	"Stims" FLOAT,
	"Sprint" FLOAT,
	"Combo" FLOAT,
	"Delay" FLOAT,
	"Attunement" FLOAT,
	"Empowered" FLOAT,
	"Burst" FLOAT,
	"Grasping" FLOAT,
	"knight" TEXT
);

TRUNCATE train_knight;
COPY train_knight("Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity", "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push", "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking", "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo", "Delay", "Attunement", "Empowered", "Burst", "Grasping", "knight")
FROM '/train_knight.csv' DELIMITER ',' CSV HEADER;

