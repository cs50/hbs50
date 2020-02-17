CREATE INDEX "birthIndex" ON "people" (
	"birth"
);

CREATE INDEX "nameIndex" ON "people" (
	"name"
);

CREATE INDEX "movieIndex" ON "stars" (
	"movie_id"
);

CREATE INDEX "personIndex" ON "stars" (
	"person_id"
);
