<?php
header('Content-Type: text/xml');
echo "<?xml version=\"1.0\" ?>\n";

$hostname = "localhost";
$username = "root";
$password = "root";
$database = "mainbatti_talika";

$db = new mysqli($hostname, $username, $password, $database);
if ($db->connect_error){
    die("Connection Failed: " . $db->connect_error);
}

$tables = array();

$query = "SELECT * FROM routine;";
if (!$result = $db->query($query)){
    die("Coulnd't run query: " . $db->error);
}

while ($row = $result->fetch_assoc()){
    $start = strtotime($row['start']);
    $end = strtotime($row['end']);
    $tables[$row['table-id']][$row['group-id']][$row['day']]['start'][] = date('h', $start).":".date('i', $start);
    $tables[$row['table-id']][$row['group-id']][$row['day']]['end'][] = date('h', $end).":".date('i', $end);
}

echo "<Routine>\n";
foreach ($tables as $tableId => $groups){
    echo "<Table>\n";
    foreach($groups as $groupId => $days){
        echo "<Group id=\"".$groupId."\">\n";
        foreach($days as $day => $times){
            $starts = $times['start'];
            $ends = $times['end'];
            echo "<".$day.">\n";
            for ($x = 0; $x < count($starts); $x++){
                echo "<Time start=\"".$starts[$x]."\" end=\"".$ends[$x]."\" />\n";
            }
            echo "</".$day.">\n";
        }
        echo "</Group>\n";
    }
    echo "</Table>\n";
}
echo "</Routine>\n";

$db->close();
?>
