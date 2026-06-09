import { describe, expect, it } from "vitest";
import {
  cn,
  formatAvg,
  formatEra,
  formatInnings,
  formatPct,
  formatWinRate,
  getGameStatusColor,
  getGameStatusLabel,
  getPositionAbbr,
  getWinRateColor,
} from "@/lib/utils";

describe("cn", () => {
  it("merges class names", () => {
    expect(cn("px-2", "py-2")).toBe("px-2 py-2");
  });
  it("resolves tailwind conflicts", () => {
    expect(cn("px-2", "px-4")).toBe("px-4");
  });
  it("handles falsy values", () => {
    expect(cn("px-2", false, undefined, null, "py-2")).toBe("px-2 py-2");
  });
});

describe("formatAvg", () => {
  it("formats with 3 decimal places dropping leading zero", () => {
    expect(formatAvg(0.325)).toBe(".325");
  });
  it("returns dash for undefined", () => {
    expect(formatAvg(undefined)).toBe("-");
  });
  it("handles 0", () => {
    expect(formatAvg(0)).toBe(".000");
  });
});

describe("formatEra", () => {
  it("formats with 2 decimal places", () => {
    expect(formatEra(3.14159)).toBe("3.14");
  });
  it("returns dash for undefined", () => {
    expect(formatEra(undefined)).toBe("-");
  });
});

describe("formatPct", () => {
  it("appends % sign", () => {
    expect(formatPct(23.5)).toBe("23.5%");
  });
  it("returns dash for undefined", () => {
    expect(formatPct(undefined)).toBe("-");
  });
});

describe("formatWinRate", () => {
  it("drops leading zero", () => {
    expect(formatWinRate(0.583)).toBe(".583");
  });
  it("formats exactly 3 decimal places", () => {
    expect(formatWinRate(0.5)).toBe(".500");
  });
});

describe("formatInnings", () => {
  it("formats whole innings", () => {
    expect(formatInnings(7)).toBe("7.0");
  });
  it("formats partial innings", () => {
    expect(formatInnings(6.2)).toBe("6.2");
  });
  it("returns dash for undefined", () => {
    expect(formatInnings(undefined)).toBe("-");
  });
});

describe("getGameStatusLabel", () => {
  it("maps known statuses", () => {
    expect(getGameStatusLabel("scheduled")).toBe("예정");
    expect(getGameStatusLabel("live")).toBe("진행중");
    expect(getGameStatusLabel("final")).toBe("종료");
    expect(getGameStatusLabel("postponed")).toBe("취소");
  });
  it("returns original string for unknown status", () => {
    expect(getGameStatusLabel("unknown")).toBe("unknown");
  });
});

describe("getGameStatusColor", () => {
  it("live is red", () => {
    expect(getGameStatusColor("live")).toContain("bg-red-500");
  });
  it("scheduled is blue", () => {
    expect(getGameStatusColor("scheduled")).toContain("bg-blue-100");
  });
});

describe("getWinRateColor", () => {
  it("high win rate is green", () => {
    expect(getWinRateColor(0.65)).toContain("green");
  });
  it("low win rate is red", () => {
    expect(getWinRateColor(0.3)).toContain("red");
  });
});

describe("getPositionAbbr", () => {
  it("translates Korean positions to abbreviations", () => {
    expect(getPositionAbbr("투수")).toBe("P");
    expect(getPositionAbbr("포수")).toBe("C");
    expect(getPositionAbbr("유격수")).toBe("SS");
    expect(getPositionAbbr("지명타자")).toBe("DH");
  });
  it("returns original string for unknown position", () => {
    expect(getPositionAbbr("알수없음")).toBe("알수없음");
  });
});
