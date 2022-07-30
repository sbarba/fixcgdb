<?php

set_error_handler(function() {}, E_ALL);
session_start();
$download_name = $_SESSION["download_name"];

// Need this header to force save rather than open.
header("Content-disposition: attachment; filename=$download_name");

header("Content-type: text/plain");
readfile($_SESSION["fixed_path"]);
unlink($_SESSION["fixed_path"]);
session_destroy();

?>
