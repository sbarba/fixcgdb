/// <reference types="Cypress" />

describe('Page Sanity', () => {
  it('shows necessary elements & in correct state', () => {
    cy.visit('/')
    cy.title().should('eq', 'CardGameDB -> OCTGN', 'Title ok')
    cy.getByTestId('upload-label').should('be.visible')
    cy.getByTestId('upload-button').should('not.be.visible')
    cy.getByTestId('upload-area').should('be.disabled')
    cy.getByTestId('upload-area').invoke('text').then(text => {
      expect(text).to.equal('')
    })
    cy.getByTestId('download-area').should('be.disabled')
    cy.getByTestId('download-area').invoke('text').then(text => {
      expect(text).to.eq('Fixed objective sets will appear here.')
    })
    cy.document().contains('stevepop')
  })
})
