<?php

session_start();

function notify($subject, $body) {
    if (gethostname() == "thomas-stone") {
        mail("stevenbarba@gmail.com", $subject, $body);
    }
}

// Extract attributes of an XML tag from a SimpleXML object.
// Put them into a normal hash and return the hash.
function attrs($xml_obj) {
    $attrs = [];
    foreach($xml_obj->attributes() as $a => $b) {
        $attrs[$a] = (string) $b;
    }
    return $attrs;
}

// Find the given objective set in the reference array.
// $octgn is the reference array (octgn.json). $value is the name of the objective from $deck.
function octgn_info($octgn, $value) {

    $correct_cards = false;
    $i = 1;
    
    // Loop through each objective set.
    foreach($octgn as $set) {
        // Loop through each card in the objective set looking for $value in objective cards.
        foreach($set["cards"] as $card) {
            // We found the objective (it's always the 1st). Add it to $correct_cards array.
            if ((in_array($value, $card)) and (array_key_exists("type", $card))) {
                $correct_cards[0] = $card;
            }
            // Add the objective's command cards to $correct_cards
            elseif ($correct_cards != false and $i <= 5)  {
                array_push($correct_cards, $card);
                $i++;
            }
        }
    }
    return $correct_cards;
}

// Convert the corrected deck into an XML-looking string.
// Note the "\r\n" since this will ultimately be a windows file.
function array_to_xml($deck) {

    foreach($deck["attrs"] as $key => $attr) {
        $xml = "<deck $key=\"$attr\"";
    }
    $xml .= ">\r\n";
    
    foreach($deck["sections"] as $section) {
        foreach($section["attrs"] as $key => $attr) {
            $xml .= "    <section $key=\"$attr\"";
            $xml .= ">\r\n";
        }
        foreach($section["cards"] as $card) {
            $xml .= "        <card";
            foreach($card["attrs"] as $key => $attr) {
                $xml .= " $key=\"$attr\"";
            }
            $xml .= ">";
            $xml .= $card["value"];
            
            $xml .= "</card>\r\n";
            
        }
        $xml .= "    </section>\r\n";
    }
    $xml .= "</deck>\r\n";
    return $xml;
}

set_error_handler(function() {}, E_ALL);

$uploaded_path = $_SESSION["uploaded_path"];

// To debug hard-code the path of a file to fix here and run fixer.php on the command line.
// $uploaded_path = '/Users/stevenbarba/Desktop/orig_55eb3aa44b46c_rebelswarm.o8d';

$x_deck = simplexml_load_file($uploaded_path);
restore_error_handler();

if (! $x_deck) {
    notify("FixCGDB Notice: Not XML", "http://deckply.com/fixcgdb/" . $uploaded_path);
    exit("Invalid File");
}
elseif ((string) $x_deck->attributes()["game"] != "d5cf89e5-1984-4873-8ae0-f06eea411bb3"){
    notify("FixCGDB Notice: Not a Star Wars file", "http://deckply.com/fixcgdb/" . $uploaded_path);
    exit("Invalid File");
}

// Convert SimpleXML object into normal array called $deck.
$deck = [];

// Use the attrs function to extract the game attribute
$deck["attrs"] = attrs($x_deck);

// Loop through each section of the deck.
$deck["sections"] = [];
foreach($x_deck->section as $x_section) {

    // Pull each section's attributes,e.g. "Command Deck".
    $section = ["attrs" => attrs($x_section)];
    
    // Loop through each card in each section.
    // Pull attributes and value and put them into
    // attrs & value arrays.
    $section["cards"] = [];
    foreach($x_section->card as $x_card) {
        $card_attrs = attrs($x_card);
        $value = (string) $x_card;
        $cards = ["attrs" => $card_attrs, "value" => $value];
        array_push($section["cards"], $cards);
    }
    // Add section to deck.
    array_push($deck["sections"], $section);
}

// Read the OCTGN JSON reference into a PHP array.
$octgn = json_decode(file_get_contents("octgn.json"), true);

// Fix deck.
$objective_deck_index = 0;
$command_deck_index = 0;
$fixes = [];

// Loop through Objective Deck section.
foreach($deck["sections"][2]["cards"] as $deck_objective) {
    // Grab the correct objective set from $octgn (the array made from octgn.json).
    $octgn_set = octgn_info($octgn, $deck_objective["value"]);
    
    // Bail if the objective name doesn't match anything in octgn.json.
    if (! $octgn_set) {
        notify("FixCGDB Notice: .o8d file, but not Star Wars", "http://deckply.com/fixcgdb/" . $uploaded_path);
        exit("Invalid File");
    }
    // The 1st card is the objective itself.
    $octgn_objective = array_shift($octgn_set);

    // If the id is incorrect...
    if ($deck_objective["attrs"]["id"] != $octgn_objective["id"]) {
        // Correct the id in $deck.
        $deck["sections"][2]["cards"][$objective_deck_index]["attrs"]["id"] = $octgn_objective["id"];
        // Push the name of the fixed objective onto the $fixes array
        // to show the user the change.
        array_push($fixes, $octgn_objective["name"]);
    }
    $objective_deck_index++;

    // Put the remaining cards from the objective set into the Commmand Deck section.
    foreach($octgn_set as $octgn_card) {
        $deck["sections"][1]["cards"][$command_deck_index]["attrs"]["id"] = $octgn_card["id"];
        $command_deck_index++;
    }
}

if (count($fixes) == 0) {
    notify("FixCGDB Notice: No fixes necessary", "http://deckply.com/fixcgdb/" . $uploaded_path);
    exit("No fixes necessary");
}

// Convert back to xml, save it, and send it to the browser.
else {
    // Start with the <?xml... line at the top of the file.
    $matches = [];
    preg_match("(<\?xml .+\?>)", file_get_contents($uploaded_path), $matches);
    $fixed_deck = $matches[0] . "\r\n" . array_to_xml($deck);
    
    // Save the fixed deck on the server.
    $fixed_path =  preg_replace("(files/orig)", "files/fixed_orig", $uploaded_path);
    file_put_contents($fixed_path, $fixed_deck);
    // Put the fixed deck's path in the $_SESSION array.
    $_SESSION["fixed_path"] = $fixed_path;

    // Echo the fixes back to the browser.
    echo "Fixed Objective Sets:\r\n";
    foreach($fixes as $fix) {
        echo "    - $fix\r\n";
    }
    echo "\r\n";
    
    // Find the download name, echo it to the browser and save it to the $_SESSIONS array.
     $_SESSION["download_name"] = "fixed_" . $_SESSION["upload_name"];
    echo $_SESSION["download_name"] . ":\r\n\r\n";
    
    // Echo the fixed deck to the client.
    notify("FixCGDB Notice: File fixed.", "http://deckply.com/fixcgdb/" . $uploaded_path);
    echo $fixed_deck;
}

?>