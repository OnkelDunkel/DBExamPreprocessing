use examdb;
alter table cities add location point;
update cities set location = point(latitude, longtitude);
alter table cities
	modify location point not null,
	add spatial index(location);