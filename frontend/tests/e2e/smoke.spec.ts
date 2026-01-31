import { test, expect } from "@playwright/test";

test.describe("Smoke", () => {
  test("homepage loads", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("h1")).toContainText("Multi-School Website Platform");
  });
});
