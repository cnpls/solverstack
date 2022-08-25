describe("My First Test", () => {
  it("Has a button on home page", () => {
    cy.visit("http://localhost:3000");
    cy.get("button.hello-world-btn").should("exist");
  });
});
