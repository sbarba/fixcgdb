/// <reference types="Cypress" />

// This script has a big timing hack. Not to be relied upon.

import 'cypress-file-upload'

function downloadWorkaround(dummySelector, testDelay, correctUploadText, correctDownloadText, reloadDelay) {
  cy.window().document().then(doc => {
    setTimeout(() => {
      expect(doc.querySelector('[data-test=upload-area]').textContent).to.equal(correctUploadText)
      expect(doc.querySelector('[data-test=download-area]').textContent).to.equal(correctDownloadText)
    }, testDelay)
    doc.addEventListener('click', () => {
      setTimeout(() => {
        doc.location.reload()
      }, reloadDelay)
    })
    cy.getByTestId(dummySelector).click()
  })
}

describe('End-to-end fix test with download workaround', () => {
  let correctUploadText = ''
  let correctDownloadText = ''

  before(() => {
    cy.visit('/')
    cy.fixture('multi_fix.o8d').then((contents) => {
      correctUploadText = contents.replace(/\r/g, '') // CardGameDB files are CRLF. On page they're LF.
    })
    cy.fixture('expected_multi_fix_fixer_response.o8d').then((contents) => {
      correctDownloadText = contents.replace(/\r/g, '')
    })
  })
  it("fixes file with multiple problems", () => {
    downloadWorkaround('upload-label', 2000, correctUploadText, correctDownloadText, 4000)
    cy.getByTestId('upload-button').attachFile('../fixtures/multi_fix.o8d')
    cy.screenshot('1', {overwrite: true})
  })
})
