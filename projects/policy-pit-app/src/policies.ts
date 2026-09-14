export type Lean = "blue" | "red" | "neutral";

export interface PolicyCard {
  id: string;
  topic: string;
  prompt: string;
  bluePosition: string;
  redPosition: string;
  sourceNote: string;
}

export const policyCards: PolicyCard[] = [
  {
    id: "clean-energy",
    topic: "Energy",
    prompt: "How should the sample candidates approach new electricity generation?",
    bluePosition: "Use public incentives to speed up renewable generation and grid storage.",
    redPosition: "Reduce permitting barriers and let competing energy producers expand supply.",
    sourceNote: "Illustrative copy only — not attributed to a real person or campaign.",
  },
  {
    id: "small-business",
    topic: "Economy",
    prompt: "How should the sample candidates support small businesses?",
    bluePosition: "Offer targeted grants and public lending for new and underserved owners.",
    redPosition: "Lower compliance costs and simplify taxes for independently owned firms.",
    sourceNote: "Illustrative copy only — not attributed to a real person or campaign.",
  },
  {
    id: "skills-training",
    topic: "Education",
    prompt: "How should the sample candidates expand career training?",
    bluePosition: "Fund community-college certificates and paid apprenticeships directly.",
    redPosition: "Give employers tax incentives to train and credential new workers.",
    sourceNote: "Illustrative copy only — not attributed to a real person or campaign.",
  },
];

export function nextIndex(current: number, total: number): number {
  return total === 0 ? 0 : Math.min(current + 1, total);
}

export function progressLabel(current: number, total: number): string {
  return current >= total ? `${total} of ${total}` : `${current + 1} of ${total}`;
}
