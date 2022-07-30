/// <reference types="Cypress" />

describe('Direct back-end testing', () => {
  const testCases = [{
    'file': 'one_fix.o8d',
    'expectedFixerResponse': 'expected_one_fix_fixer_response.o8d',
    'expectedDownloadResponse': 'expected_one_fix_download_response.o8d'
  }, {
    'file': 'multi_fix.o8d',
    'expectedFixerResponse': 'expected_multi_fix_fixer_response.o8d',
    'expectedDownloadResponse': 'expected_multi_fix_download_response.o8d'
  }, {
    'file': 'curly_quote.o8d',
    'expectedFixerResponse': 'expected_curly_quote_fixer_response.o8d',
    'expectedDownloadResponse': 'expected_curly_quote_download_response.o8d'
  }, {
    'file': '漢字.o8d',
    'expectedFixerResponse': 'expected_漢字_fixer_response.o8d',
    'expectedDownloadResponse': 'expected_one_fix_download_response.o8d'
  }]

  for (const tc of testCases) {
    it(`uploads, fixes & downloads ${tc.file} correctly`, () => {
      // Have to do all this in one it() block to keep the session alive.

      cy.fixture(tc.file).then((uploadContents) => {
        cy.request(`/upload.php?fileName=${tc.file}&fileContent=${uploadContents.replace(/&/g, '%26')}`).then(r => {

          cy.log('Test what fixer.php sends back to page for #download-area')
          cy.request('fixer.php').then(r => {
            cy.fixture(tc.expectedFixerResponse).then(expectedFixerResponse => {
              expect(r.body).to.equal(expectedFixerResponse)
            })
          })

          cy.request('download.php').then(r => {
            cy.fixture(tc.expectedDownloadResponse).then(expectedDownloadResponse => {
              expect(r.body).to.equal(expectedDownloadResponse)
            })
          })
        })
      })
    })
  }
})
