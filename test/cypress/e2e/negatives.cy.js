/// <reference types="Cypress" />

import 'cypress-file-upload'

/*
Can do front-end testing with negatives because fixcgdb.js knows not to redirect to download.php
which would make Cypress wait for a file that never gets downloaded.
*/

describe('Negatives', () => {
  const testCases = [{
    'description': 'empty file',
    'file': 'empty_file.o8d',
    'expectedFixerResponse': 'Invalid File',
    'expectedDownloadResponse': ''
  }, {
    'description': 'good file',
    'file': 'expected_multi_fix_download_response.o8d',
    'expectedFixerResponse': 'No fixes necessary',
    'expectedDownloadResponse': ''
  }, {
    'description': `a file that's too big`,
    'file': 'too_big.md',
    'expectedFixerResponse': 'Invalid File',
    'expectedDownloadResponse': ''
  }, {
    'description': 'binary file',
    'file': 'binary.o8d',
    'expectedFixerResponse': 'Invalid File',
    'expectedDownloadResponse': ''
  }, {
    'description': 'non-XML file',
    'file': 'not_xml.txt',
    'expectedFixerResponse': 'Invalid File',
    'expectedDownloadResponse': ''
  }, {
    'description': 'generic XML file',
    'file': 'valid_xml_but_not.o8d',
    'expectedFixerResponse': 'Invalid File',
    'expectedDownloadResponse': ''
  }, {
    'description': 'non-SW .o8d file',
    'file': 'valid_netrunner.o8d',
    'expectedFixerResponse': 'Invalid File',
    'expectedDownloadResponse': ''
  }, {
    'description': 'file with bad objective name',
    'file': 'bad_objective_name.o8d',
    'expectedFixerResponse': 'Invalid File',
    'expectedDownloadResponse': ''
  }]

  before(() => {
    cy.visit('/')
  })
  for (const tc of testCases) {
    it(`doesn't try to fix ${tc.description}`, () => {
      // Have to do all this in one it() block to keep the session alive.
      cy.getByTestId('upload-button').attachFile({filePath: tc.file, allowEmpty: true})
      cy.fixture(tc.file).then(uploadContent => {
        cy.getByTestId('upload-area').should($uploadArea => {
          expect($uploadArea.text()).to.equal(uploadContent.replace(/\r/g, ''))
        })
      })
      cy.getByTestId('download-area').should($downloadArea => {
        expect($downloadArea.text()).to.equal(tc.expectedFixerResponse)
      })
      cy.request('download.php').then(r => {
          expect(r.body).to.equal('')
      })
    })
  }
  it(`returns error if fixer.php called directly`, () => {
    cy.request('fixer.php').then(r => {
      expect(r.body).to.eq('Invalid File')
    })
  })

  it(`returns nothing if download.php called directly`, () => {
    cy.request('download.php').then(r => {
      expect(r.body).to.eq('')
    })
  })
})
