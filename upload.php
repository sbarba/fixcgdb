<?php

session_start();

function sanitize($content) {
    $content = str_replace("’", "'", $content);
    $content = str_replace("“", "'", $content);
    $content = str_replace("”", "'", $content);
    return $content;
}

// Need to initialize this in case it has a value left over from previous uploads.
$_SESSION["uploaded_path"] = "";

$upload_name = $_GET["fileName"];
$upload_content = sanitize($_GET["fileContent"]);
$_SESSION["upload_name"] = ltrim($upload_name);

// Save uploaded file with a unique id, e.g. "files/orig_54349cfd5c48e_JediGamor.o8d".
$uploaded_path =  "files/orig_" . uniqid() . "_" . $upload_name;
file_put_contents($uploaded_path, $upload_content);
// $return = "$upload_content";

// Save the path in the $_SESSION array for other scripts.
$_SESSION["uploaded_path"] = $uploaded_path;

// Return a message to the client.
// echo $return;

?>
