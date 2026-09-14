import { describe, expect, it } from "vitest";
import { nextIndex, policyCards, progressLabel } from "./policies";

describe("policy preview data", () => {
  it("contains unique, clearly illustrative cards", () => {
    expect(new Set(policyCards.map(({ id }) => id)).size).toBe(policyCards.length);
    expect(policyCards.every(({ sourceNote }) => sourceNote.includes("Illustrative"))).toBe(true);
  });

  it("advances without exceeding the card count", () => {
    expect(nextIndex(0, 3)).toBe(1);
    expect(nextIndex(3, 3)).toBe(3);
    expect(nextIndex(0, 0)).toBe(0);
  });

  it("reports one-based progress and completion", () => {
    expect(progressLabel(0, 3)).toBe("1 of 3");
    expect(progressLabel(3, 3)).toBe("3 of 3");
  });
});
