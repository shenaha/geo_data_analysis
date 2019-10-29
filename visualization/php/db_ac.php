<?php

	$dbconn = pg_connect("host=130.75.67.35 dbname=webgis user=stud password=stud")	or die("Connection error: " . pg_last_error());
	$north1=pg_escape_string($dbconn,$_POST['var1']);
	$south1=pg_escape_string($dbconn,$_POST['var2']);
	$east1=pg_escape_string($dbconn,$_POST['var3']);
	$west1=pg_escape_string($dbconn,$_POST['var4']);
	
	$query = "SELECT osm_id, name, amenity, ST_AsGeoJSON(ST_Transform(ST_Simplify(way,1),4326)) as geometry  FROM planet_osm_point  WHERE way is not null and amenity='parking';";
								
	$result = pg_query($dbconn,$query) or die("Query error: " . pg_last_error());


	
$numResults     = pg_num_rows($result);
$counter        = 0;
$json_variable = array();

while ($row = pg_fetch_array($result)) {
    $feature = array(
        'id' => $row['osm_id'],
        'type' => 'Feature',
        'geometry' => json_decode($row['geometry']),
        'properties' => array(
        'name' => $row['name'],
        'amenity' => $row['amenity']

		
        )
    );
    array_push($json_variable, $feature);
}
header('Content-type: application/json');
echo json_encode($json_variable, JSON_NUMERIC_CHECK);
pg_free_result($result);
pg_close($dbconn);
?>