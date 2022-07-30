function upload() {
  const fileInput = document.querySelector(`#upload-button`);

  // Read file.
  const reader = new FileReader();
  reader.readAsText(fileInput.files[0]);

  // Display file, upload to server, call fix().
  reader.onload = async () => {
    document.querySelector(`#upload-area`).innerHTML = reader.result;
    await fetch(`upload.php?fileName=${fileInput.files[0]['name']}&fileContent=${encodeURIComponent(reader.result)}`);
    // document.querySelector(`#upload-area`).innerHTML = await uploadResponse.text()
    fix();

    // Clear fileInput. Otherwise it won't process a file with the same name twice, a commmon use case.
    fileInput.value = null;
  }
}

async function fix() {
  // Fix file if necessary.
  const response = await fetch(`fixer.php`);
  
  // Ouptut fixed file or error message to page.
  const fixerResponse = await response.text();
  document.querySelector(`#download-area`).innerHTML = fixerResponse;

  // Download fixed file.
  if ((fixerResponse != `Invalid File`) && (fixerResponse != `No fixes necessary`)) {
    location.href = `download.php`;
  }
}
