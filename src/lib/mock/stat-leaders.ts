// Mock data - 수치는 예시입니다
import type { StatLeader } from "@/lib/types/kbo";

export const MOCK_STAT_LEADERS: StatLeader[] = [
  {
    category: "타율",
    unit: "",
    leaders: [
      { rank: 1, playerId: "kia-003", playerName: "김도영", teamId: "KIA", teamName: "KIA 타이거즈", value: 0.319 },
      { rank: 2, playerId: "samsung-001", playerName: "구자욱", teamId: "SAMSUNG", teamName: "삼성 라이온즈", value: 0.322 },
      { rank: 3, playerId: "kiwoom-001", playerName: "이정후", teamId: "KIWOOM", teamName: "키움 히어로즈", value: 0.322 },
      { rank: 4, playerId: "lg-001", playerName: "오스틴 딘", teamId: "LG", teamName: "LG 트윈스", value: 0.318 },
      { rank: 5, playerId: "nc-001", playerName: "손아섭", teamId: "NC", teamName: "NC 다이노스", value: 0.313 },
    ],
  },
  {
    category: "홈런",
    unit: "개",
    leaders: [
      { rank: 1, playerId: "kia-003", playerName: "김도영", teamId: "KIA", teamName: "KIA 타이거즈", value: 32 },
      { rank: 2, playerId: "hanwha-003", playerName: "노시환", teamId: "HANWHA", teamName: "한화 이글스", value: 29 },
      { rank: 3, playerId: "ssg-001", playerName: "최정", teamId: "SSG", teamName: "SSG 랜더스", value: 28 },
      { rank: 4, playerId: "lg-001", playerName: "오스틴 딘", teamId: "LG", teamName: "LG 트윈스", value: 24 },
      { rank: 5, playerId: "samsung-001", playerName: "구자욱", teamId: "SAMSUNG", teamName: "삼성 라이온즈", value: 24 },
    ],
  },
  {
    category: "OPS",
    unit: "",
    leaders: [
      { rank: 1, playerId: "kia-003", playerName: "김도영", teamId: "KIA", teamName: "KIA 타이거즈", value: 0.999 },
      { rank: 2, playerId: "lg-001", playerName: "오스틴 딘", teamId: "LG", teamName: "LG 트윈스", value: 0.963 },
      { rank: 3, playerId: "ssg-001", playerName: "최정", teamId: "SSG", teamName: "SSG 랜더스", value: 0.958 },
      { rank: 4, playerId: "samsung-001", playerName: "구자욱", teamId: "SAMSUNG", teamName: "삼성 라이온즈", value: 0.956 },
      { rank: 5, playerId: "kt-001", playerName: "강백호", teamId: "KT", teamName: "KT 위즈", value: 0.912 },
    ],
  },
  {
    category: "ERA",
    unit: "",
    isLowerBetter: true,
    leaders: [
      { rank: 1, playerId: "samsung-002", playerName: "오승환", teamId: "SAMSUNG", teamName: "삼성 라이온즈", value: 2.12 },
      { rank: 2, playerId: "kia-001", playerName: "이의리", teamId: "KIA", teamName: "KIA 타이거즈", value: 2.78 },
      { rank: 3, playerId: "ssg-002", playerName: "김광현", teamId: "SSG", teamName: "SSG 랜더스", value: 2.98 },
      { rank: 4, playerId: "kt-002", playerName: "소형준", teamId: "KT", teamName: "KT 위즈", value: 3.15 },
      { rank: 5, playerId: "lotte-002", playerName: "찰리 반즈", teamId: "LOTTE", teamName: "롯데 자이언츠", value: 3.21 },
    ],
  },
  {
    category: "탈삼진",
    unit: "개",
    leaders: [
      { rank: 1, playerId: "kia-001", playerName: "이의리", teamId: "KIA", teamName: "KIA 타이거즈", value: 172 },
      { rank: 2, playerId: "ssg-002", playerName: "김광현", teamId: "SSG", teamName: "SSG 랜더스", value: 152 },
      { rank: 3, playerId: "kiwoom-002", playerName: "안우진", teamId: "KIWOOM", teamName: "키움 히어로즈", value: 145 },
      { rank: 4, playerId: "kt-002", playerName: "소형준", teamId: "KT", teamName: "KT 위즈", value: 148 },
      { rank: 5, playerId: "lotte-002", playerName: "찰리 반즈", teamId: "LOTTE", teamName: "롯데 자이언츠", value: 142 },
    ],
  },
  {
    category: "WAR",
    unit: "",
    leaders: [
      { rank: 1, playerId: "kia-001", playerName: "이의리", teamId: "KIA", teamName: "KIA 타이거즈", value: 5.2 },
      { rank: 2, playerId: "samsung-001", playerName: "구자욱", teamId: "SAMSUNG", teamName: "삼성 라이온즈", value: 4.8 },
      { rank: 3, playerId: "ssg-002", playerName: "김광현", teamId: "SSG", teamName: "SSG 랜더스", value: 4.8 },
      { rank: 4, playerId: "ssg-001", playerName: "최정", teamId: "SSG", teamName: "SSG 랜더스", value: 4.5 },
      { rank: 5, playerId: "lg-001", playerName: "오스틴 딘", teamId: "LG", teamName: "LG 트윈스", value: 4.2 },
    ],
  },
];
