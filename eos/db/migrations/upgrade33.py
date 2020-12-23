"""
Migration 33

Allow use of floats in damage pattern values
"""

tmpTable = """
CREATE TABLE "damagePatternsTemp" (
	"ID" INTEGER NOT NULL,
	"name" VARCHAR,
	"emAmount" FLOAT,
	"thermalAmount" FLOAT,
	"kineticAmount" FLOAT,
	"explosiveAmount" FLOAT,
	"ownerID" INTEGER,
	"created" DATETIME,
	"modified" DATETIME,
	PRIMARY KEY ("ID"),
	FOREIGN KEY("ownerID") REFERENCES users ("ID")
)
"""


def upgrade(saveddata_engine):
    saveddata_engine.execute(tmpTable)
    saveddata_engine.execute(
            'INSERT INTO damagePatternsTemp (ID, name, emAmount, thermalAmount, kineticAmount, explosiveAmount, ownerID, created, modified) '
            'SELECT ID, name, emAmount, thermalAmount, kineticAmount, explosiveAmount, ownerID, created, modified FROM damagePatterns')
    saveddata_engine.execute('DROP TABLE damagePatterns')
    saveddata_engine.execute('ALTER TABLE damagePatternsTemp RENAME TO damagePatterns')
