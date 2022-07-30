const assert = require('assert');
const axios = require('axios');
const jsdom = require("jsdom");
const JSDOM = jsdom.JSDOM;

let axiosResponse = axios.get('http://localhost:8888/fixcgdb/');

it('get returns 200', done => {
  axiosResponse.then(axiosResponse => {
    assert.equal(axiosResponse.status, 200);
    done();
  });
});


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
  it(`${testCase.title} is ${testCase.expected}.`, done => {
      axiosResponse.then(axiosResponse => {
        console.log('hello', testCase.expected)
        assert.equal(testCase.prop(axiosResponse), testCase.expected);
        done();
      });
  });
}

