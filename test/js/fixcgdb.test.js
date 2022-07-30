/* Jest won't work with axios unless you add a testEnvironment property to 
config. In this case I added it to package.json like this:
  "jest": {
      "testEnvironment": "node"
  }
*/

const axios = require('axios');
const request = require('sync-request');
const jsdom = require("jsdom");
const JSDOM = jsdom.JSDOM;

// Async examples
let axiosResponse = axios.get('http://localhost:8888/fixcgdb/');

test(`Home page: get returns 200 with then`, () => {
  return axiosResponse.then(axiosResponse => expect(axiosResponse.status).toBe(200));
});

// I think I prefer 'then' syntax for consistency, but here's an example of 'resolves'.
test(`Home page: get returns 200 with resolves`, () => {
  return expect(axiosResponse).resolves.toHaveProperty('status', 200);
});


/* Parameterized example using async axios:
testCases has a title, a function to grab the property to test, and an expected value.
Each test calls the function with the promised result of axios.get (axiosResponse) as
its argument. */

let testCases = [
  {title: 'Status', prop: axiosResponse => axiosResponse.status, expected: 200},
  {title: 'Status text', prop: axiosResponse => axiosResponse.statusText, expected: `OK`},
  {title: 'Title', prop:
    axiosResponse => {
      let dom = new JSDOM(axiosResponse.data);
      return dom.window.document.title;
    },
    expected: `CardGameDB -> OCTGN`}
];

for (let testCase of testCases) {
  test(`${testCase.title} is ${testCase.expected}.`, () => {
    return axiosResponse.then(axiosResponse => expect(testCase.prop(axiosResponse)).toBe(testCase.expected));
  })
}


// Synchronous examples
let requestResponse = request('GET', 'http://localhost:8888/fixcgdb/');

test(`Home page: Synchronous get returns 200 with then`, () => {
  expect(requestResponse.statusCode).toBe(200);
});

testCases = [
  {title: 'Status', prop: requestResponse => requestResponse.statusCode, expected: 200},
  {title: 'Title', prop:
    requestResponse => {
      let dom = new JSDOM(requestResponse.body.toString());
      return dom.window.document.title;
    },
    expected: `CardGameDB -> OCTGN`}
];

for (let testCase of testCases) {
  test(`${testCase.title} is ${testCase.expected}.`, () => {
    expect(testCase.prop(requestResponse)).toBe(testCase.expected);
  })
}
