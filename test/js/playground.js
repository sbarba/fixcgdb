const axios = require('axios');

let axiosResponse = axios.get('http://localhost:8888/fixcgdb/');

axiosResponse.then(axiosResponse => {
  console.log(axiosResponse.status);
})